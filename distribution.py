"""Computes observed digit distribution and theoretical Benford distribution."""

import math


def benford_expected():
    """Returns {digit: expected_percentage} per Benford's Law."""
    return {d: math.log10(1 + 1 / d) * 100 for d in range(1, 10)}


def benford_expected_second_digit():
    """
    Returns {digit: expected_percentage} for the second significant digit
    per Benford's Law.

    P(d2) = sum_{d1=1}^{9} log10(1 + 1/(10*d1 + d2))
    """
    result = {}
    for d2 in range(0, 10):
        prob = sum(math.log10(1 + 1 / (10 * d1 + d2)) for d1 in range(1, 10))
        result[d2] = prob * 100
    return result


def observed_distribution(digits):
    """Returns (counts, percentages) for digits 1-9 given a list of leading digits."""
    total = len(digits)
    counts = {d: 0 for d in range(1, 10)}

    for d in digits:
        counts[d] += 1

    if total == 0:
        percentages = {d: 0.0 for d in range(1, 10)}
    else:
        percentages = {d: (counts[d] / total) * 100 for d in range(1, 10)}

    return counts, percentages


def observed_distribution_second_digit(digits):
    """Returns (counts, percentages) for digits 0-9 given a list of second digits."""
    total = len(digits)
    counts = {d: 0 for d in range(0, 10)}

    for d in digits:
        counts[d] += 1

    if total == 0:
        percentages = {d: 0.0 for d in range(0, 10)}
    else:
        percentages = {d: (counts[d] / total) * 100 for d in range(0, 10)}

    return counts, percentages
