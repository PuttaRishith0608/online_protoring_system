"""
Simple logging service for the application
"""
import logging
from datetime import datetime

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("ProctorSystem")


def log_info(message: str, user_id: str = None, extra_data: dict = None):
    """Log info level message"""
    msg = f"[{user_id}] {message}" if user_id else message
    if extra_data:
        msg += f" | {extra_data}"
    logger.info(msg)


def log_error(message: str, user_id: str = None, extra_data: dict = None):
    """Log error level message"""
    msg = f"[{user_id}] {message}" if user_id else message
    if extra_data:
        msg += f" | {extra_data}"
    logger.error(msg)


def log_warning(message: str, user_id: str = None, extra_data: dict = None):
    """Log warning level message"""
    msg = f"[{user_id}] {message}" if user_id else message
    if extra_data:
        msg += f" | {extra_data}"
    logger.warning(msg)


def log_debug(message: str, user_id: str = None, extra_data: dict = None):
    """Log debug level message"""
    msg = f"[{user_id}] {message}" if user_id else message
    if extra_data:
        msg += f" | {extra_data}"
    logger.debug(msg)
