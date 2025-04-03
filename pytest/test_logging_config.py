import logging
import os
import pytest
from src.app.logging_config import configure_logger


@pytest.fixture
def clean_log_file():
    log_file = './app.log'
    if os.path.exists(log_file):
        os.remove(log_file)
    yield
    if os.path.exists(log_file):
        os.remove(log_file)


def test_configure_logger_creates_logger():
    logger = configure_logger("buba")
    assert logger is not None
    assert logger.name == "buba"


def test_configure_logger_sets_log_level(clean_log_file):
    logger = configure_logger("buba", log_level=logging.INFO)
    assert logger.level == logging.INFO
    assert logger.level != logging.DEBUG


def test_configure_logger_adds_console_handler(clean_log_file):
    logger = configure_logger("buba")
    handlers = logger.handlers
    assert any(
        isinstance(handler, logging.StreamHandler) for handler in handlers
        )
    assert not any(
        isinstance(handler, logging.NullHandler) for handler in handlers
        )


def test_configure_logger_creates_log_file(clean_log_file):
    log_file = './app.log'
    logger = configure_logger("buba", log_file=log_file)
    assert os.path.exists(log_file)


def test_configure_logger_logs_messages(clean_log_file):
    log_file = './app.log'
    logger = configure_logger("buba", log_file=log_file)

    logger.info("Test message")

    with open(log_file, 'r') as f:
        log_content = f.read()

    assert "Test message" in log_content
