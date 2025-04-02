import configparser
import os

from .logging_config import configure_logger

logger = configure_logger(__name__)

required_vars_set = {'log_dir',
                     'report_dir',
                     'report_size',
                     'report_template_path'}


def check_config_exists(filename):
    """Function to check file existance"""
    if not os.path.isfile(filename):
        logger.error(f"Config file {filename} does not exist.")
    return os.path.isfile(filename)


def read_config(config_path):
    """Function to read config file and return dict"""
    config = configparser.ConfigParser()
    logger.info(f"Try to read config file {config_path}")
    try:
        config.read(config_path)
        variables = dict(config['DEFAULT'])
        logger.info(f"Read success from config file {config_path}")
        return variables
    except Exception as e:
        logger.error(f"Error reading {config_path}: {e}")


def check_all_vars_set(available_vars):
    """Function to check availability of all vars"""
    available_vars_set = set(available_vars)
    missing_vars = required_vars_set - available_vars_set
    logger.info("Try to compare AVAILABLE and REQUIRED variables")
    if missing_vars:
        logger.error(f"Required variable(-s) missing: "
                            f"{', '.join(missing_vars)}"
                            )
        return False
    logger.info("All REQUIRED variables available")
    return True
