"""Compares observed vs expected distributions and produces a verdict."""

DEVIATION_THRESHOLD = 5.0      # avg abs % difference above this = flagged
CHI2_CRITICAL_VALUE = 15.51    # chi-square critical value, df=8, p=0.05


def mean_absolute_deviation(observed_pct, expected_pct):
    """Average absolute percentage-point difference across all digits."""
    diffs = [abs(observed_pct[d] - expected_pct[d]) for d in observed_pct]
    return sum(diffs) / len(diffs)


def chi_square_statistic(observed_counts, expected_pct, total):
    """
    Standard chi-square goodness-of-fit statistic.
    expected_count for digit d = expected_pct[d]/100 * total
    """
    chi2 = 0.0
    for d in observed_counts:
        expected_count = (expected_pct[d] / 100) * total
        if expected_count == 0:
            continue
        chi2 += ((observed_counts[d] - expected_count) ** 2) / expected_count
    return chi2


def get_verdict(score, method):
    if method == "chi2":
        if score <= CHI2_CRITICAL_VALUE:
            return "MATCH", "Matches Benford's Law -- data appears natural."
        return "DEVIATION", "Significant deviation (chi-square) -- possible manipulation."
    else:
        if score <= DEVIATION_THRESHOLD:
            return "MATCH", "Matches Benford's Law -- data appears natural."
        return "DEVIATION", "Significant deviation -- possible manipulation."
