import argparse
import sys

from src.app.config import (
    read_config,
    check_all_vars_set)
from src.app.log_stuff import (
    get_latest_log_file_name,
    process_log)
from src.app.report_stuff import (
    prepare_data,
    form_report
)

config = "default_config.ini"


def main():
    config_dict = read_config(config)
    if not config_dict:
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Script to parse logs "
                                                 "(custom config included)")
    parser.add_argument("--config", help="Path to extra config file")
    args = parser.parse_args()
    if args.config:
        custom_config = read_config(args.config)
        config_dict.update(custom_config)

    if not check_all_vars_set(config_dict.keys()):
        sys.exit(1)
    else:
        log_dir = config_dict["log_dir"]
        print(f"log_dir: {log_dir}")
        report_dir = config_dict["report_dir"]
        print(f"report_dir: {report_dir}")
        report_size = int(config_dict["report_size"])
        print(f"report_size: {report_size}")
        report_template_path = config_dict["report_template_path"]
        print(f"report_template_path: {report_template_path}")

    log_file = get_latest_log_file_name(log_dir)
    log_file_path = f"{log_dir}/{log_file}"
    result = process_log(log_file_path)
    report_data = prepare_data(result)
    form_report(
        report_data,
        report_dir=report_dir,
        report_template_path=report_template_path)


if __name__ == "__main__":
    main()
