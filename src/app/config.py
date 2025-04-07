import configparser
import os

required_vars_set = {
    "log_dir",
    "report_dir",
    "report_size",
    "report_template_path",
}


def check_config_exists(filename):
    """Function to check file existance"""
    try:
        return os.path.isfile(filename)
    except Exception as e:
        raise RuntimeError(
            "An unexpected error occurred "
            + f"while checking existence of {filename}"
        ) from e


def read_config(config_path):
    """Function to read config file and return dict"""
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        variables = dict(config["DEFAULT"])
        return variables
    except Exception as e:
        raise RuntimeError(
            "An unexpected error occurred " + f"while reading {config_path}"
        ) from e


def check_all_vars_set(available_vars):
    """Function to check availability of all vars"""
    try:
        available_vars_set = set(available_vars)
        missing_vars = required_vars_set - available_vars_set
        return missing_vars
    except TypeError:
        raise TypeError("Available variables must be an iterable")
    except Exception as e:
        raise RuntimeError(
            "An unexpected error occurred " "while checking the variables"
        ) from e
