import json
import os


def get_from_data(filename):
    tests_path = os.path.split(__file__)[0]
    data_for_tests_path = os.path.join("/", tests_path, "data_for_tests", filename)
    with open(data_for_tests_path, "r", encoding="utf-8") as f:
        return f.read()


def get_json_from_data(filename):
    return json.loads(get_from_data(filename))
