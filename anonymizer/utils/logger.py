import logging
import sys

def setup_logger(name: str, log_level: str = "DEBUG"):
    """
    Creates and configures a logger with the given name and log level.

    Args:
        name (str): Name of the logger (usually `__name__` from the calling module).
        log_level (str): Logging level (e.g., "DEBUG", "INFO", "ERROR").

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger
