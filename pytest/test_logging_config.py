import logging
import os

from src.app.logging_config import configure_logger


class LogFileManager:
    def __init__(self, log_file):
        self.log_file = log_file

    def __enter__(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)


def test_configure_logger_creates_logger():
    logger = configure_logger("buba")
    assert logger is not None
    assert logger.name == "buba"


def test_configure_logger_sets_log_level():
    logger = configure_logger("buba", log_level=logging.INFO)
    assert logger.level == logging.INFO
    assert logger.level != logging.DEBUG


def test_configure_logger_adds_console_handler():
    logger = configure_logger("buba")
    handlers = logger.handlers
    assert any(
        isinstance(handler, logging.StreamHandler) for handler in handlers
    )
    assert not any(
        isinstance(handler, logging.NullHandler) for handler in handlers
    )


def test_configure_logger_creates_log_file():
    log_file = "./app.log"
    with LogFileManager(log_file):
        logger = configure_logger("buba", log_file=log_file)
        logger.info("Test message")
        assert os.path.exists(log_file)


def test_configure_logger_logs_messages():
    log_file = "./app.log"
    with LogFileManager(log_file):
        logger = configure_logger("buba", log_file=log_file)
        logger.info("Test message")
        with open(log_file, "r") as f:
            log_content = f.read()
        assert "Test message" in log_content
