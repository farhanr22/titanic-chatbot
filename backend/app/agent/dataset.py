import os
import urllib.request
from app.core.logging import app_logger

DATASET_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/refs/heads/master/titanic.csv"
DATASET_PATH = "/data/titanic.csv"  # Docker volume


async def setup_dataset():
    os.makedirs("/data", exist_ok=True)
    if not os.path.exists(DATASET_PATH):
        app_logger.info(f"Downloading dataset from {DATASET_URL}")
        urllib.request.urlretrieve(DATASET_URL, DATASET_PATH)
        app_logger.info("Dataset downloaded successfully.")
    else:
        app_logger.info("Dataset already exists.")
