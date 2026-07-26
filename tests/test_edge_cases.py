"""Edge-case tests -- zeros, negatives, non-numeric junk, empty inputs."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from digit_extractor import (
    extract_leading_digit,
    extract_second_digit,
    extract_all_digits,
    extract_all_second_digits,
)


class TestAllZeros:
    """A column of all zeros should produce an empty digit list."""

    def test_leading_digits_from_zeros(self):
        values = [0, 0.0, "0", "0.00"]
        assert extract_all_digits(values) == []

    def test_second_digits_from_zeros(self):
        values = [0, 0.0, "0", "0.00"]
        assert extract_all_second_digits(values) == []


class TestNegativeNumbers:
    """Negative numbers should be handled by absolute value."""

    def test_leading_digits(self):
        values = [-1, -23, -456, -0.078]
        result = extract_all_digits(values)
        assert result == [1, 2, 4, 7]

    def test_second_digits(self):
        values = [-12, -345, -0.078]
        result = extract_all_second_digits(values)
        assert result == [2, 4, 8]


class TestNonNumericJunk:
    """Non-numeric strings, None, special chars should be silently filtered."""

    def test_mixed_csv_like_data(self):
        values = [
            "hello", "N/A", "", None, "---",
            "1234", "56.78", "not a number",
            "0.001", "NaN",  # Python's float("NaN") is valid but 0-ish
        ]
        result = extract_all_digits(values)
        # "1234" -> 1, "56.78" -> 5, "0.001" -> 1
        assert result == [1, 5, 1]

    def test_second_digit_junk(self):
        values = ["hello", None, "", "42", "7"]
        result = extract_all_second_digits(values)
        # "42" -> 2, "7" -> None (single digit)
        assert result == [2]


class TestEmptyInput:
    def test_empty_list_leading(self):
        assert extract_all_digits([]) == []

    def test_empty_list_second(self):
        assert extract_all_second_digits([]) == []


class TestSpecialFloats:
    def test_very_small_number(self):
        assert extract_leading_digit(0.000000001) == 1

    def test_very_large_number(self):
        assert extract_leading_digit(9999999999) == 9

    def test_inf_returns_none(self):
        assert extract_leading_digit(float("inf")) is None

    def test_nan_returns_none(self):
        assert extract_leading_digit(float("nan")) is None
