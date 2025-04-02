from src.app.config import read_config

from src.app.log_stuff import (
    get_latest_log_file_name,
    process_log)
from src.app.report_stuff import (
    prepare_data,
    form_report
)

config = "default_config.ini"
required_vars = ('log_dir',
                 'report_dir',
                 'report_size',
                 'report_template_path')

config_dict = read_config(config)

log_dir = config_dict["log_dir"]
report_dir = config_dict["report_dir"]
report_size = config_dict["report_size"]
report_template_path = config_dict["report_template_path"]


def main():
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
