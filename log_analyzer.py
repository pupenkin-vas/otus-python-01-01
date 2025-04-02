import configparser

from src.app.log_stuff import (
    get_latest_log_file_name,
    process_log)
from src.app.report_stuff import (
    prepare_data,
    form_report
)

config = configparser.ConfigParser()
config.read('default_config.ini')

LOG_DIR = config['DEFAULT']['LOG_DIR']
REPORT_DIR = config['DEFAULT']["REPORT_DIR"]
REPORT_SIZE = config.getint('DEFAULT', "REPORT_SIZE")
REPORT_TEMPLATE_PATH = config['DEFAULT']["REPORT_TEMPLATE_PATH"]


def main():
    log_file = get_latest_log_file_name(LOG_DIR)
    log_file_path = f"{LOG_DIR}/{log_file}"
    result = process_log(log_file_path)
    js = prepare_data(result)
    form_report(
        js,
        report_dir=REPORT_DIR,
        report_template_path=REPORT_TEMPLATE_PATH)


if __name__ == "__main__":
    main()
