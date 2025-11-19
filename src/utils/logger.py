"""
Logging configuration and utilities.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from src.config.settings import LOG_LEVEL, LOG_FILE


def setup_logger(
    name: str = "catawiki_scraper", log_file: Optional[str] = None, level: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: Logger name
        log_file: Optional log file path (uses config default if None)
        level: Log level (uses config default if None)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set level
    log_level = getattr(logging, (level or LOG_LEVEL).upper())
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler
    file_path = log_file or LOG_FILE
    if file_path:
        try:
            # Ensure log directory exists
            log_path = Path(file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(file_path, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not setup file logging: {e}")

    return logger


# Create default logger instance
logger = setup_logger()
