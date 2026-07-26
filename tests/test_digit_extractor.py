"""Tests for digit_extractor.py -- leading and second digit extraction."""

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


# ── extract_leading_digit ──────────────────────────────────────────────

class TestExtractLeadingDigit:
    def test_positive_integer(self):
        assert extract_leading_digit(1234) == 1

    def test_large_number(self):
        assert extract_leading_digit(999999) == 9

    def test_float(self):
        assert extract_leading_digit(3.14) == 3

    def test_negative_number(self):
        assert extract_leading_digit(-56.3) == 5

    def test_tiny_decimal(self):
        assert extract_leading_digit(0.0089) == 8

    def test_zero_returns_none(self):
        assert extract_leading_digit(0) is None

    def test_zero_float_returns_none(self):
        assert extract_leading_digit(0.0) is None

    def test_string_number(self):
        assert extract_leading_digit("4567") == 4

    def test_string_float(self):
        assert extract_leading_digit("0.072") == 7

    def test_non_numeric_string_returns_none(self):
        assert extract_leading_digit("hello") is None

    def test_none_input_returns_none(self):
        assert extract_leading_digit(None) is None

    def test_empty_string_returns_none(self):
        assert extract_leading_digit("") is None

    def test_single_digit(self):
        assert extract_leading_digit(5) == 5

    def test_leading_digit_is_one_through_nine(self):
        for d in range(1, 10):
            assert extract_leading_digit(d * 100) == d


# ── extract_second_digit ──────────────────────────────────────────────

class TestExtractSecondDigit:
    def test_normal_integer(self):
        assert extract_second_digit(1234) == 2

    def test_tiny_decimal(self):
        assert extract_second_digit(0.0089) == 9

    def test_negative(self):
        assert extract_second_digit(-56.3) == 6

    def test_single_digit_returns_none(self):
        assert extract_second_digit(5) is None

    def test_zero_returns_none(self):
        assert extract_second_digit(0) is None

    def test_non_numeric_returns_none(self):
        assert extract_second_digit("abc") is None

    def test_none_returns_none(self):
        assert extract_second_digit(None) is None

    def test_two_digit_number(self):
        assert extract_second_digit(42) == 2

    def test_second_digit_is_zero(self):
        assert extract_second_digit(100) == 0

    def test_string_input(self):
        assert extract_second_digit("7890") == 8


# ── extract_all_digits ────────────────────────────────────────────────

class TestExtractAllDigits:
    def test_filters_invalid(self):
        values = [123, "hello", None, 0, 456]
        result = extract_all_digits(values)
        assert result == [1, 4]

    def test_empty_list(self):
        assert extract_all_digits([]) == []

    def test_all_invalid(self):
        assert extract_all_digits(["foo", "bar", None]) == []


# ── extract_all_second_digits ─────────────────────────────────────────

class TestExtractAllSecondDigits:
    def test_filters_single_digit(self):
        values = [5, 42, 300]
        result = extract_all_second_digits(values)
        # 5 -> None (skipped), 42 -> 2, 300 -> 0
        assert result == [2, 0]

    def test_empty_list(self):
        assert extract_all_second_digits([]) == []
