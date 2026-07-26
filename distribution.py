"""Computes observed digit distribution and theoretical Benford distribution."""

import math


def benford_expected():
    """Returns {digit: expected_percentage} per Benford's Law."""
    return {d: math.log10(1 + 1 / d) * 100 for d in range(1, 10)}


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
