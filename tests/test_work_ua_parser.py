from types import SimpleNamespace
from unittest import mock

from tests.utils import get_json_from_data, get_from_data
from work_ua_parser import get_jobs

file_by_url_start = {
    "https://www.work.ua/jobs-": "response.html",
    "https://www.work.ua/jobs/": "response-details.html",
}


def mock_get(url):
    for k, v in file_by_url_start.items():

        if url.startswith(k):
            html = get_from_data(v)

    mock_response = SimpleNamespace()
    mock_response.text = html
    return mock_response


def test_get_jobs():
    expected_result = get_json_from_data("expected_job.json")

    with mock.patch("requests.get", new=mock_get):
        jobs = get_jobs("", "")

    assert jobs == expected_result
