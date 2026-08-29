import json
import os
import aiosqlite
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.agent.tools import tools
from app.core.config import settings
from app.agent.prompt import system_prompt
from app.core.logging import app_logger

# Global instance
_agent_executor = None
_db_conn = None


async def init_agent():
    """Initialize the agent executor once at startup"""
    global _agent_executor, _db_conn

    os.makedirs("/history", exist_ok=True)
    _db_conn = await aiosqlite.connect("/history/history.db")
    memory = AsyncSqliteSaver(_db_conn)

    extra_body = None
    if settings.MODEL_EXTRA_BODY:
        try:
            extra_body = json.loads(settings.MODEL_EXTRA_BODY)
        except json.JSONDecodeError as e:
            app_logger.warning(f"Failed to parse MODEL_EXTRA_BODY JSON: {e}")

    llm_kwargs = {
        "model": settings.MODEL_NAME,
        "temperature": settings.MODEL_TEMPERATURE,
        "openai_api_base": settings.OPENAI_API_BASE,
        "api_key": settings.OPENAI_API_KEY,
        "max_retries": 3,
        "timeout": 15.0,
    }

    if settings.MODEL_TOP_P is not None:
        llm_kwargs["top_p"] = settings.MODEL_TOP_P

    if extra_body:
        llm_kwargs["extra_body"] = extra_body

    llm = ChatOpenAI(**llm_kwargs)

    _agent_executor = create_agent(
        llm, tools, system_prompt=system_prompt, checkpointer=memory
    )
    return _agent_executor


async def get_agent_executor():
    """Get the initialized agent executor"""
    if _agent_executor is None:
        raise RuntimeError("Agent not initialized. Call init_agent() first.")
    return _agent_executor


async def close_agent():
    """Clean up resources"""
    global _db_conn
    if _db_conn:
        await _db_conn.close()
