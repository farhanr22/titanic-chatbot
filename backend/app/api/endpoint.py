from fastapi import APIRouter, Depends, Response, status
from app.core.schemas import ChatRequest, APIResponse
from app.agent import get_agent_executor
from app.core.security import verify_token
from app.core.logging import app_logger

router = APIRouter()


@router.post("/chat", dependencies=[Depends(verify_token)], response_model=APIResponse)
async def chat_endpoint(request: ChatRequest, response: Response):
    """
    Waits for the agent to finish completely before returning the final text and artifact.
    """
    app_logger.info(
        f"Starting agent run for session: {request.session_id} with user input : {request.user_input}"
    )

    executor = await get_agent_executor()

    inputs = {"messages": [("user", request.user_input)]}
    config = {"configurable": {"thread_id": request.session_id}, "recursion_limit": 15}

    try:
        result = await executor.ainvoke(inputs, config=config)
        messages = result.get("messages", [])

        final_text = ""
        artifact = None

        # Parse the message history in reverse
        # to grab the latest AI text and the latest Tool artifact
        for msg in reversed(messages):
            # Stop looking backward once we hit the user's current prompt
            if msg.type == "human":
                break

            # Grab the AI text
            if msg.type == "ai" and msg.content and not final_text:
                final_text = msg.content

            # Grab the Tool artifact
            elif (
                msg.type == "tool"
                and hasattr(msg, "artifact")
                and msg.artifact
                and not artifact
            ):
                artifact = msg.artifact

            if final_text and artifact:
                break

        app_logger.info("Agent run complete. Returning final payload.")

        return APIResponse(
            success=True, data={"text": final_text, "artifact": artifact}
        )

    except Exception as e:
        app_logger.error(f"Agent execution failed: {e}", exc_info=True)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return APIResponse(
            success=False,
            error={"message": "Agent execution failed", "details": str(e)},
        )
