"""Extracts the leading (first significant) digit from a number."""


def extract_leading_digit(value):
    """
    Returns the first non-zero digit of a number, ignoring sign,
    decimal point, and leading zeros.

    Examples:
        1234    -> 1
        0.0089  -> 8
        -56.3   -> 5
    """
    try:
        num = abs(float(value))
    except (ValueError, TypeError):
        return None

    if num == 0:
        return None

    # Convert to string, strip sign/decimal point, drop leading zeros
    s = f"{num:.10f}".replace(".", "").lstrip("0")

    if not s:
        return None

    return int(s[0])


def extract_all_digits(values):
    """Applies extract_leading_digit to a list, dropping invalid entries."""
    digits = []
    for v in values:
        d = extract_leading_digit(v)
        if d is not None and 1 <= d <= 9:
            digits.append(d)
    return digits
