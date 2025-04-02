import configparser


required_vars_set = {'log_dir',
                     'report_dir',
                     'report_size',
                     'report_template_path'}


def read_config(config_path):
    """Function to read config file and return dict"""
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        variables = dict(config['DEFAULT'])
        return variables
    except (configparser.Error, FileNotFoundError) as e:
        print(f"Error reading {config_path}: {e}")


def check_all_vars_set(current_vars):
    """Function to check availability of all vars"""
    current_vars_set = set(current_vars)
    missing_vars = required_vars_set - current_vars_set
    if missing_vars:
        print(f"Required variable(-s) missing: "
              f"{', '.join(missing_vars)}"
              )
        return False
    return True
