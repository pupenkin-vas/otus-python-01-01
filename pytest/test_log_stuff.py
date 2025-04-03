from unittest import mock

from src.app.log_stuff import (
    get_date_from_filename,
    get_latest_log_file_name,
    parse_log_content,
    process_log,
)


def test_get_latest_log_file_name():
    log_dir = "test_logs"
    mock_files = [
        "nginx-access-ui.log-20250402.gz",
        "nginx-access-ui.log-20250403",
    ]

    with mock.patch("os.listdir", return_value=mock_files):
        latest_file = get_latest_log_file_name(log_dir)
        assert latest_file == "nginx-access-ui.log-20250403"


def test_get_date_from_filename():
    filename = "nginx-access-ui.log-20250403.gz"
    date = get_date_from_filename(filename)
    assert date == "20250403"


def test_parse_log_content():
    log_lines = [
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET '
        + '/api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 '
        + 'libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" '
        + '"1498697422-2190034393-4708-9752759" "dc7161be3" 0.390',
        "1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "
        + '"GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 '
        + 'HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" '
        + '"1498697422-32900793-4708-9752770" "-" 0.133',
    ]

    log_file = mock.mock_open(read_data="\n".join(log_lines))

    with log_file() as f:
        result = parse_log_content(f)
        assert result["total_requests"] == 2
        assert result["total_request_time"] == 0.523
        assert "/api/v2/banner/25019354", [0.39] in result[
            "log_entries"
        ].items()
        assert "/api/1/photogenic_banners/list/?server_name=WIN7RB4", [
            0.133
        ] in result["log_entries"].items()


def test_process_log():
    log_filename = "nginx-access-ui.log-20250403.gz"
    log_lines = [
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET '
        + '/api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 '
        + 'libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" '
        + '"1498697422-2190034393-4708-9752759" "dc7161be3" 0.390',
    ]

    with mock.patch(
        "gzip.open", mock.mock_open(read_data="\n".join(log_lines))
    ):
        result = process_log(log_filename)
        assert result is not None
        assert result["total_requests"] == 1
        assert result["total_request_time"] == 0.390
