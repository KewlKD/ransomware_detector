from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler


DEFAULT_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(message)s"
)

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    level="INFO",
    log_directory="logs",
    log_filename="application.log",
):
    """
    Configure and return the application logger.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR)

    log_directory : str
        Directory where log files are stored.

    log_filename : str
        Name of the log file.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger("RansomwareDetector")

    # Prevent duplicate handlers if called multiple times.
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    Path(log_directory).mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Rotating file output
    file_handler = RotatingFileHandler(
        Path(log_directory) / log_filename,
        maxBytes=2 * 1024 * 1024,   # 2 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


def get_logger():
    """
    Return the configured logger.
    """

    return logging.getLogger("RansomwareDetector")
    ...