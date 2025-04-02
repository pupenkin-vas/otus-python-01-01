from src.app.log_stuff import (
    get_latest_log_file_name,
    process_log)
from src.app.report_stuff import (
    prepare_data,
    form_report
)


config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./REPORT_DIR",
    "LOG_DIR": "./LOG_DIR"
}

LOG_DIR = "./LOG_DIR"


def main():
    log_file = get_latest_log_file_name(LOG_DIR)
    log_file_path = f"{LOG_DIR}/{log_file}"
    result = process_log(log_file_path)
    js = prepare_data(result)
    form_report(js)


if __name__ == "__main__":
    main()
