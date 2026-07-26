"""Tests for distribution.py -- Benford expected values and observed distributions."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from distribution import (
    benford_expected,
    benford_expected_second_digit,
    observed_distribution,
    observed_distribution_second_digit,
)


# ── benford_expected ──────────────────────────────────────────────────

class TestBenfordExpected:
    def test_sums_to_100(self):
        pct = benford_expected()
        assert sum(pct.values()) == pytest.approx(100.0, abs=0.01)

    def test_digit_1_is_highest(self):
        pct = benford_expected()
        assert pct[1] > pct[2] > pct[3]

    def test_has_nine_digits(self):
        pct = benford_expected()
        assert set(pct.keys()) == set(range(1, 10))

    def test_digit_1_approximately_30(self):
        pct = benford_expected()
        assert 30.0 < pct[1] < 30.2


# ── benford_expected_second_digit ─────────────────────────────────────

class TestBenfordExpectedSecondDigit:
    def test_sums_to_100(self):
        pct = benford_expected_second_digit()
        assert sum(pct.values()) == pytest.approx(100.0, abs=0.01)

    def test_has_ten_digits(self):
        pct = benford_expected_second_digit()
        assert set(pct.keys()) == set(range(0, 10))

    def test_flatter_than_first_digit(self):
        """Second-digit distribution is much flatter than first-digit."""
        pct1 = benford_expected()
        pct2 = benford_expected_second_digit()
        spread1 = max(pct1.values()) - min(pct1.values())
        spread2 = max(pct2.values()) - min(pct2.values())
        assert spread2 < spread1


# ── observed_distribution ─────────────────────────────────────────────

class TestObservedDistribution:
    def test_known_list(self):
        digits = [1, 1, 1, 2, 2, 3]
        counts, pcts = observed_distribution(digits)
        assert counts[1] == 3
        assert counts[2] == 2
        assert counts[3] == 1
        assert pcts[1] == pytest.approx(50.0)

    def test_empty_list(self):
        counts, pcts = observed_distribution([])
        assert all(c == 0 for c in counts.values())
        assert all(p == 0.0 for p in pcts.values())


# ── observed_distribution_second_digit ────────────────────────────────

class TestObservedDistributionSecondDigit:
    def test_known_list(self):
        digits = [0, 0, 5, 9]
        counts, pcts = observed_distribution_second_digit(digits)
        assert counts[0] == 2
        assert counts[5] == 1
        assert counts[9] == 1
        assert pcts[0] == pytest.approx(50.0)

    def test_empty_list(self):
        counts, pcts = observed_distribution_second_digit([])
        assert all(c == 0 for c in counts.values())
