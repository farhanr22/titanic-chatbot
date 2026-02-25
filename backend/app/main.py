from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.api.endpoint import router
from app.core.logging import app_logger
from contextlib import asynccontextmanager
from app.agent import init_agent, close_agent
from app.core.exceptions import (
    global_exception_handler,
    validation_exception_handler,
    custom_http_exception_handler,
)
from app.agent.dataset import setup_dataset


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_dataset()  # Run dataset setup logic
    await init_agent()  # Intialize agent executor
    app_logger.info("Agent executor and dataset loaded.")
    yield
    await close_agent()  # Shutdown


app = FastAPI(title="Titanic Agent API", lifespan=lifespan)

# Register Error Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)


# Register endpoint
app.include_router(router, prefix="/api")
