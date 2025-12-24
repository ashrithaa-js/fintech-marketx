import logging
import os

# Ensure logs directory exists
os.makedirs("data/logs", exist_ok=True)

logging.basicConfig(
    filename="data/logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    logging.info(msg)

def get_logger(name):
    """Get a logger instance for a module"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler("data/logs/system.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
