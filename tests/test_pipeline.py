# tests/test_pipeline.py

import pytest
from CSV_report2 import find_country_code, format_date, calculate_clicks 


def test_find_country_code_known():
    code = find_country_code("United States")
    assert isinstance(code, str) and len(code) == 3


def test_find_country_code_unknown():
    code = find_country_code("Atlantis")
    assert code == "XXX"


def test_format_date():
    assert format_date("12/31/2020") == "2020-12-31"
    assert format_date("01/01/2021") == "2021-01-01"


def test_calculate_clicks():
    assert calculate_clicks("1000", "2.5%") == 25
    assert calculate_clicks("2000", "10%") == 200
