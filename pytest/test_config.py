import os
import pytest
from unittest.mock import patch
from src.app.config import (
    check_config_exists,
    read_config,
    check_all_vars_set
    )

TEST_CONFIG_FILE = 'test_config.ini'


@pytest.fixture
def create_test_config_file():
    with open(TEST_CONFIG_FILE, 'w') as f:
        f.write("[DEFAULT]\n")
        f.write("log_dir = /var/log\n")
        f.write("report_dir = /var/report\n")
        f.write("report_size = 10MB\n")
        f.write("report_template_path = /path/to/template\n")
    yield
    os.remove(TEST_CONFIG_FILE)


def test_check_config_exists(create_test_config_file):
    assert check_config_exists(TEST_CONFIG_FILE) is True
    assert check_config_exists('TESTO_CONFIG_FILE.ini') is False


@patch('configparser.ConfigParser.read')
@patch('configparser.ConfigParser.__getitem__',
       return_value={
           'log_dir': '/var/log',
           'report_dir': '/var/report',
           'report_size': '10MB',
           'report_template_path': '/path/to/template'
        }
       )
def test_read_config(mock_getitem, mock_read, create_test_config_file):
    config = read_config(TEST_CONFIG_FILE)
    assert config['log_dir'] == '/var/log'
    assert config['report_dir'] == '/var/report'
    assert config['report_size'] == '10MB'
    assert config['report_template_path'] == '/path/to/template'


@patch('src.app.config.logger')
def test_check_all_vars_set(mock_logger):
    available_vars = ['log_dir', 'report_dir']
    assert check_all_vars_set(available_vars) is False
    assert "Required variable(-s) missing" in str(mock_logger.error.call_args)

    available_vars = ['log_dir',
                      'report_dir',
                      'report_size',
                      'report_template_path'
                      ]
    assert check_all_vars_set(available_vars) is True
    assert "All REQUIRED variables available" in str(
        mock_logger.info.call_args
        )
