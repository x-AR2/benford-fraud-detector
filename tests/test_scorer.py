"""Tests for scorer.py -- MAD, chi-square, and verdicts."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from scorer import (
    mean_absolute_deviation,
    chi_square_statistic,
    get_verdict,
    CHI2_CRITICAL_VALUE,
)
from distribution import benford_expected


# ── mean_absolute_deviation ───────────────────────────────────────────

class TestMAD:
    def test_identical_distributions_zero(self):
        pct = {d: 11.1 for d in range(1, 10)}
        assert mean_absolute_deviation(pct, pct) == pytest.approx(0.0)

    def test_known_difference(self):
        obs = {d: 10.0 for d in range(1, 10)}
        exp = {d: 12.0 for d in range(1, 10)}
        assert mean_absolute_deviation(obs, exp) == pytest.approx(2.0)

    def test_mixed_differences(self):
        obs = {1: 30.0, 2: 20.0, 3: 10.0, 4: 10.0, 5: 10.0,
               6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0}
        exp = benford_expected()
        result = mean_absolute_deviation(obs, exp)
        assert result > 0
        assert isinstance(result, float)


# ── chi_square_statistic ─────────────────────────────────────────────

class TestChiSquare:
    def test_perfect_match_near_zero(self):
        """When observed counts exactly match expected, chi2 ~ 0."""
        exp = benford_expected()
        total = 1000
        counts = {d: round((exp[d] / 100) * total) for d in range(1, 10)}
        stat = chi_square_statistic(counts, exp, total)
        assert stat < 1.0  # allow small rounding error

    def test_large_deviation(self):
        """Uniform counts should produce a large chi2."""
        exp = benford_expected()
        total = 900
        counts = {d: 100 for d in range(1, 10)}
        stat = chi_square_statistic(counts, exp, total)
        assert stat > 50  # clearly significant

    def test_critical_value_is_15_51(self):
        """Verify the hardcoded critical value is as expected."""
        assert CHI2_CRITICAL_VALUE == 15.51


# ── get_verdict ───────────────────────────────────────────────────────

class TestGetVerdict:
    def test_chi2_match(self):
        verdict, msg = get_verdict(10.0, "chi2")
        assert verdict == "MATCH"
        assert "natural" in msg.lower()

    def test_chi2_deviation(self):
        verdict, msg = get_verdict(20.0, "chi2")
        assert verdict == "DEVIATION"
        assert "chi-square" in msg.lower()

    def test_chi2_at_boundary(self):
        verdict, _ = get_verdict(15.51, "chi2")
        assert verdict == "MATCH"

    def test_chi2_just_above(self):
        verdict, _ = get_verdict(15.52, "chi2")
        assert verdict == "DEVIATION"

    def test_mad_match(self):
        verdict, msg = get_verdict(3.0, "mad")
        assert verdict == "MATCH"

    def test_mad_deviation(self):
        verdict, msg = get_verdict(6.0, "mad")
        assert verdict == "DEVIATION"

    def test_mad_boundary(self):
        verdict, _ = get_verdict(5.0, "mad")
        assert verdict == "MATCH"
