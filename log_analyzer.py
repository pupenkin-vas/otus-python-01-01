import argparse
import sys

from src.app.config import (
    read_config,
    check_all_vars_set,
    check_config_exists)
from src.app.log_stuff import (
    get_latest_log_file_name,
    process_log,
    get_date_from_filename)
from src.app.report_stuff import (
    prepare_data,
    form_report
)
from src.app.logging_config import configure_logger, cleanup_logger


config = "default_config.ini"


def main():
    logger = configure_logger(__name__)
    if not check_config_exists(config):
        logger.error(f"Config file {config} not exists")
        sys.exit(1)

    try:
        logger.info(f"Reading {config}")
        config_dict = read_config(config)
    except Exception as e:
        logger.error(f"Error while reading {config}: e")
        raise e

    parser = argparse.ArgumentParser(description="Script to parse logs "
                                                 "(custom config included)")
    parser.add_argument("--config", help="Path to extra config file")
    args = parser.parse_args()
    if args.config and check_config_exists(args.config):
        custom_config = read_config(args.config)
        config_dict.update(custom_config)

    missing_vars = check_all_vars_set(config_dict.keys())

    if missing_vars:
        logger.error("Error while reading config: "
                     "Missing required variable(s): "
                     f"{', '.join(missing_vars)}")
        sys.exit(1)

    logger.info("All REQUIRED variables available")
    log_dir = config_dict["log_dir"]
    report_dir = config_dict["report_dir"]
    report_size = int(config_dict["report_size"])
    report_template_path = config_dict["report_template_path"]
    if "app_log_path" in config_dict.keys():
        cleanup_logger(__name__)
        app_log_path = config_dict["app_log_path"]
        logger = configure_logger(
            __name__,
            log_file=app_log_path)

    logger.info(f"Searching recent log in {log_dir}")
    try:
        log_file = get_latest_log_file_name(log_dir)
        logger.info(f"Log file: {log_file}")
        log_data = get_date_from_filename(log_file)
        logger.info(f"Log data: {log_data}")
    except Exception as e:
        logger.error("Error while searching "
                     f"recent log: {e}")
        sys.exit(1)

    log_file_path = f"{log_dir}/{log_file}"
    logger.info(f"Processing {log_file_path}")
    try:
        result = process_log(log_file_path)
        logger.info(f"Processing {log_file_path} complete")
    except Exception as e:
        logger.error("Error while processing "
                     f"log_file {log_file_path}: {e}")
        sys.exit(1)

    logger.info("Preparing report")
    try:
        logger.info("Preparing data for report")
        report_data = prepare_data(result)
        logger.info("Start forming report")
        form_report(
            report_data,
            report_dir=report_dir,
            report_template_path=report_template_path,
            log_data=log_data)
        logger.info("Report is ready")
    except Exception as e:
        logger.error("Error while preparing "
                     f"report: {e}")


if __name__ == "__main__":
    main()
