from src.app.report_stuff import prepare_data, pretty_digitizer


def test_pretty_digitizer():
    assert pretty_digitizer(1) == "1.000000"
    assert pretty_digitizer(1.23456789) == "1.234568"
    assert pretty_digitizer(0) == "0.000000"
    assert pretty_digitizer(-1.234) == "-1.234000"


def test_prepare_data():
    log_data = {
        "total_requests": 5,
        "total_request_time": 10,
        "log_entries": {
            "http://buba.com": [1, 2, 3],
            "http://biba.com": [2, 2],
        },
    }

    expected_result = [
        {
            "url": "http://buba.com",
            "count": 3,
            "count_perc": "0.600000",
            "time_sum": "6.000000",
            "time_perc": "0.600000",
            "time_avg": "2.000000",
            "time_max": "3.000000",
            "time_med": "2.000000",
        },
        {
            "url": "http://biba.com",
            "count": 2,
            "count_perc": "0.400000",
            "time_sum": "4.000000",
            "time_perc": "0.400000",
            "time_avg": "2.000000",
            "time_max": "2.000000",
            "time_med": "2.000000",
        },
    ]

    report_size = 2
    result = prepare_data(log_data, report_size)
    assert result == expected_result

    report_size = 1
    expected_result_single = [expected_result[0]]
    result_single = prepare_data(log_data, report_size)
    assert result_single == expected_result_single
