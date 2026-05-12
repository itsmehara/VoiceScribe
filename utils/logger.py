import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.whisper_config import LOG_FOLDER


def get_logger(logger_name: str = "voicescribe_logger") -> logging.Logger:
    """
    Creates and returns reusable logger instance.
    Supports:
    - Rotating file logs
    - Console logs
    """

    log_directory = Path(LOG_FOLDER)
    log_directory.mkdir(exist_ok=True)

    log_file_path = log_directory / "voicescribe.log"

    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(filename)s:%(lineno)d | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ----------------------------------------
    # Rotating File Handler
    # ----------------------------------------

    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )

    file_handler.setFormatter(log_formatter)

    # ----------------------------------------
    # Console Handler
    # ----------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(log_formatter)

    # ----------------------------------------
    # Add Handlers
    # ----------------------------------------

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger