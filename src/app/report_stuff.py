import statistics
import string

from .logging_config import configure_logger

logger = configure_logger(__name__)


def pretty_digitizer(digit):
    """Function to transform ugly-non-human to readable"""
    return f"{digit:.6f}"


def prepare_data(log_data):
    """Function, that get a dict and born an appropriate list"""
    logger.info("Preparing data for report")
    total_requests = log_data["total_requests"]
    total_request_time = log_data["total_request_time"]
    result = []
    for url, time_list in log_data["log_entries"].items():
        result.append({
            "url": url,
            "count": len(time_list),
            "count_perc": pretty_digitizer(len(time_list) / total_requests),
            "time_sum": pretty_digitizer(sum(time_list)),
            "time_perc": pretty_digitizer(sum(time_list) / total_request_time),
            "time_avg": pretty_digitizer(statistics.fmean(time_list)),
            "time_max": pretty_digitizer(max(time_list)),
            "time_med": pretty_digitizer(statistics.median(time_list))
        })
    logger.info("Preparing data complete")
    return result


def form_report(data_result,
                report_dir,
                report_template_path,
                log_data):
    """Function, that get a list, born a report and write it on disk"""
    logger.info("Start forming report")
    with open(report_template_path, 'r') as file:
        template_file = file.read()
    template = string.Template(template_file)
    html_report = template.safe_substitute(table_json=data_result)
    current_date = f"{log_data[:4]}.{log_data[4:6]}.{log_data[6:]}"
    report_file_path = f'{report_dir}/report-{current_date}.html'

    with open(report_file_path, 'w', encoding='utf-8') as f:
        f.write(html_report)

    logger.info(f"Report available {report_file_path}")
