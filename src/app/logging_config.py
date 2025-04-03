import logging
import os
import structlog


def configure_logger(app_name, log_level=logging.INFO, log_file=None):
    """Function to init logger"""
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
            structlog.processors.add_log_level,
            structlog.processors.EventRenamer("msg"),
            structlog.stdlib.add_logger_name,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),

    )

    logger = structlog.get_logger(app_name)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter("%(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def cleanup_logger(app_name):
    """Function to completely remove logger"""
    logger = structlog.get_logger(app_name)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    logging.getLogger(app_name).handlers.clear()
    logging.Logger.manager.loggerDict.pop(app_name, None)
