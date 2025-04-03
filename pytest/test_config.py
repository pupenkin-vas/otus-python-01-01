import os
from unittest.mock import patch

from src.app.config import check_all_vars_set, check_config_exists, read_config

TEST_CONFIG_FILE = "test_config.ini"


def create_test_config_file():
    with open(TEST_CONFIG_FILE, "w") as f:
        f.write("[DEFAULT]\n")
        f.write("log_dir = /var/log\n")
        f.write("report_dir = /var/report\n")
        f.write("report_size = 10MB\n")
        f.write("report_template_path = /path/to/template\n")


def remove_test_config_file():
    if os.path.exists(TEST_CONFIG_FILE):
        os.remove(TEST_CONFIG_FILE)


def test_check_config_exists():
    create_test_config_file()
    try:
        assert check_config_exists(TEST_CONFIG_FILE) is True
        assert check_config_exists("TESTO_CONFIG_FILE.ini") is False
    finally:
        remove_test_config_file()


@patch("configparser.ConfigParser.read")
@patch(
    "configparser.ConfigParser.__getitem__",
    return_value={
        "log_dir": "/var/log",
        "report_dir": "/var/report",
        "report_size": "10MB",
        "report_template_path": "/path/to/template",
    },
)
def test_read_config(mock_getitem, mock_read):
    create_test_config_file()
    try:
        config = read_config(TEST_CONFIG_FILE)
        assert config["log_dir"] == "/var/log"
        assert config["report_dir"] == "/var/report"
        assert config["report_size"] == "10MB"
        assert config["report_template_path"] == "/path/to/template"
    finally:
        remove_test_config_file()


def test_check_all_vars_set():
    available_vars = ["log_dir", "report_dir"]
    assert check_all_vars_set(available_vars) == {
        "report_size",
        "report_template_path",
    }

    available_vars = [
        "log_dir",
        "report_dir",
        "report_size",
        "report_template_path",
    ]
    assert bool(check_all_vars_set(available_vars)) is False
