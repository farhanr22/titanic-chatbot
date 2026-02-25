from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import error_logger
from app.core.schemas import APIResponse


async def global_exception_handler(request: Request, exc: Exception):
    error_logger.error(f"Unhandled Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            error={"message": "Internal Server Error", "details": str(exc)},
        ).dict(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Catch Pydantic validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIResponse(
            success=False,
            error={"message": "Validation Error", "details": exc.errors()},
        ).dict(),
    )


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Catch and deal with FastAPI HTTPExceptions like 401 (security)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            error={
                "message": f"Client Error ({exc.status_code})",
                "details": exc.detail,
            },
        ).dict(),
    )