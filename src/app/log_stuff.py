import gzip
import os
import re

FILE_NAME_REGEX = re.compile(r"^nginx-access-ui\.log-(\d{8})(\.gz)?$")
LOG_LINE_REGEX = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # addr
                            r"\s(.*?)\s(.*?)"  # $remote_user $http_x_real_ip
                            r"\s\[(\d{1,2}\/[A-Za-z]{3}\/\d{4}"  # day
                            r":\d{2}:\d{2}:\d{2}\s[+\-]\d{4})\]"  # time
                            r"\s\"(.*?)\s(.*?)\s(.*?)\""  # "request"
                            r"\s(\d+)\s(\d+)\s\"(.*?)\""  # status sent ...
                            r"\s\"(.*?)\"\s\"(.*?)\"\s\"(.*?)\"\s\"(.*?)\""
                            r"\s(\d+\.\d+)$")  # request_time


def get_latest_log_file_name(log_dir, name_regex=FILE_NAME_REGEX):
    """Function to get most recent log filename"""
    try:
        return max(
                f_name for f_name in os.listdir(log_dir)
                if name_regex.match(f_name)
                )
    except Exception as e:
        raise e


def get_date_from_filename(filename):
    """Function to extract date from filename"""
    try:
        match = FILE_NAME_REGEX.match(filename)
        log_date = match.group(1)
        return log_date
    except Exception as e:
        raise e


def parse_log_content(log_file, line_regex=LOG_LINE_REGEX):
    """Function to parse log file content"""
    log_entries = {}
    total_requests = 0
    total_request_time = 0
    try:
        for line in log_file:
            match = re.match(line_regex, line)
            if match:
                url = match.group(6)
                request_time = float(match.group(15))
                total_requests += 1
                total_request_time += request_time
                if url not in log_entries:
                    log_entries[url] = []
                log_entries[url].append(request_time)
        return {'log_entries': log_entries,
                'total_requests': total_requests,
                'total_request_time': total_request_time}
    except Exception as e:
        raise e


def process_log(log_filename):
    """Head function ('extract' log content, make it parsed)"""
    opener = gzip.open if log_filename.endswith(".gz") else open
    try:
        with opener(log_filename, 'rt') as f:
            log_data = parse_log_content(f)
            if not log_data:
                return None

            return log_data
    except Exception as e:
        raise e
