import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists (mounted via Docker)
os.makedirs("/logs", exist_ok=True)


def setup_logging():
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # App specific logger
    app_logger = logging.getLogger("app_logger")
    app_logger.setLevel(logging.INFO)
    app_handler = RotatingFileHandler(
        "/logs/app.log", maxBytes=1 * 1024 * 1024, backupCount=3
    )
    app_handler.setFormatter(log_formatter)
    app_logger.addHandler(app_handler)

    # Error logger
    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.ERROR)
    error_handler = RotatingFileHandler(
        "/logs/error.log", maxBytes=1 * 1024 * 1024, backupCount=3
    )
    error_handler.setFormatter(log_formatter)
    error_logger.addHandler(error_handler)

    # Uvicorn override
    uvicorn_logger = logging.getLogger("uvicorn.error")
    uvicorn_handler = RotatingFileHandler(
        "/logs/uvicorn.log", maxBytes=1 * 1024 * 1024, backupCount=3
    )
    uvicorn_handler.setFormatter(log_formatter)
    uvicorn_logger.addHandler(uvicorn_handler)

    return app_logger, error_logger


app_logger, error_logger = setup_logging()
