"""Extracts the leading (first significant) digit from a number."""

import math


def _significant_digits_str(value):
    """
    Convert value to a string of significant digits (no sign, no decimal,
    no leading zeros). Returns None for invalid / non-finite values.
    """
    try:
        num = abs(float(value))
    except (ValueError, TypeError):
        return None

    if num == 0 or math.isnan(num) or math.isinf(num):
        return None

    # Convert to string, strip sign/decimal point, drop leading zeros
    s = f"{num:.10f}".replace(".", "").lstrip("0")

    if not s:
        return None

    return s


def extract_leading_digit(value):
    """
    Returns the first non-zero digit of a number, ignoring sign,
    decimal point, and leading zeros.

    Examples:
        1234    -> 1
        0.0089  -> 8
        -56.3   -> 5
    """
    s = _significant_digits_str(value)
    if s is None:
        return None
    return int(s[0])


def extract_second_digit(value):
    """
    Returns the second significant digit of a number (0-9), or None
    if the number has only one significant digit.

    Examples:
        1234    -> 2
        100     -> 0
        0.0089  -> 9
        -56.3   -> 6
        5       -> None  (single significant digit)
    """
    try:
        num = abs(float(value))
    except (ValueError, TypeError):
        return None

    s = _significant_digits_str(value)
    if s is None:
        return None

    if num >= 1:
        # For numbers >= 1, trailing zeros are real digits (e.g. 100 has
        # three digits).  Use the magnitude to count.
        n_digits = math.floor(math.log10(num)) + 1
        if n_digits < 2:
            return None
    else:
        # For numbers < 1, trailing zeros in the fixed-point string are
        # formatting artefacts (e.g. 0.005 -> "50000000000").
        if len(s.rstrip("0")) < 2:
            return None

    return int(s[1])


def extract_all_digits(values):
    """Applies extract_leading_digit to a list, dropping invalid entries."""
    digits = []
    for v in values:
        d = extract_leading_digit(v)
        if d is not None and 1 <= d <= 9:
            digits.append(d)
    return digits


def extract_all_second_digits(values):
    """Applies extract_second_digit to a list, dropping invalid entries."""
    digits = []
    for v in values:
        d = extract_second_digit(v)
        if d is not None and 0 <= d <= 9:
            digits.append(d)
    return digits
