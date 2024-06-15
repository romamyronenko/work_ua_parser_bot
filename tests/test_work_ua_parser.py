import json
from types import SimpleNamespace
from unittest import mock

from work_ua_parser import get_jobs

file_by_url_start = {
    "https://www.work.ua/jobs-": "response.html",
    "https://www.work.ua/jobs/": "response-details.html",
}


def mock_get(url):
    for k, v in file_by_url_start.items():

        if url.startswith(k):
            with open(f"data_for_tests/{v}", "r", encoding="utf-8") as f:
                html = f.read()

    mock_response = SimpleNamespace()
    mock_response.text = html
    return mock_response


def test_get_jobs():
    with open("data_for_tests/expected_job.json", "r") as f:
        expected_result = json.loads(f.read())

    with mock.patch("requests.get", new=mock_get):
        jobs = get_jobs("", "")

    assert jobs == expected_result
