from loguru import logger
import sys


def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        backtrace=False,
        diagnose=False,
        format="<green>{time}</green> | <level>{level}</level> | {message}",
    )
    return logger


logger = setup_logging()
