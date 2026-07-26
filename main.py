#!/usr/bin/env python
"""
Benford's Law Fraud Detector
-----------------------------
A CLI tool that checks whether a dataset's leading-digit distribution
matches Benford's Law -- a heuristic used in real forensic accounting
and fraud audits.

Usage examples:
    python main.py --generate natural
    python main.py --generate random
    python main.py --file sample_data/world_populations.csv --column population
    python main.py --file sample_data/tampered_expenses.csv --column amount --test chi2
"""

import argparse
import csv
import sys

from digit_extractor import (
    extract_all_digits,
    extract_all_second_digits,
)
from distribution import (
    benford_expected,
    benford_expected_second_digit,
    observed_distribution,
    observed_distribution_second_digit,
)
from scorer import (
    mean_absolute_deviation,
    chi_square_statistic,
    get_verdict,
)
from visualizer import render_chart
from data_generator import generate_natural_data, generate_random_data


AUTO_CHI2_THRESHOLD = 50  # minimum sample size for chi-square reliability


def load_from_csv(filepath, column):
    values = []
    try:
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            if column not in reader.fieldnames:
                print(f"Error: column '{column}' not found. "
                      f"Available columns: {reader.fieldnames}")
                sys.exit(1)
            for row in reader:
                values.append(row[column])
    except FileNotFoundError:
        print(f"Error: file '{filepath}' not found.")
        sys.exit(1)
    return values


def _resolve_method(requested, n):
    """
    Resolves the actual scoring method based on the user's request and
    the sample size.  Returns (method, explanation_message_or_None).
    """
    if requested == "auto":
        if n >= AUTO_CHI2_THRESHOLD:
            return "chi2", f"Auto-selected chi-square (n={n} >= {AUTO_CHI2_THRESHOLD})"
        else:
            return "mad", (f"Auto-selected MAD (n={n} < {AUTO_CHI2_THRESHOLD}; "
                           f"chi-square is unreliable below ~{AUTO_CHI2_THRESHOLD} samples)")

    if requested == "chi2" and n < AUTO_CHI2_THRESHOLD:
        return "mad", (f"Note: Chi-square is unreliable for samples below "
                       f"{AUTO_CHI2_THRESHOLD} (n={n}). "
                       f"Falling back to MAD (mean absolute deviation).")

    return requested, None


def _score_and_verdict(counts, observed_pct, expected_pct, n, method):
    """
    Computes score and verdict for a single digit test.
    Returns (score, verdict, message).
    """
    if method == "chi2":
        score = chi_square_statistic(counts, expected_pct, n)
    else:
        score = mean_absolute_deviation(observed_pct, expected_pct)

    verdict, message = get_verdict(score, method)
    return score, verdict, message


def _method_display_name(method):
    if method == "chi2":
        return "Chi-square goodness-of-fit"
    return "Mean absolute deviation (MAD)"


def _print_result_block(title, n, method, score, verdict, message):
    """Prints a single analysis result block."""
    print(f"\n=== {title} ===")
    print(f"Sample size: {n}")
    print(f"Method: {_method_display_name(method)}")
    print(f"Score: {score:.2f}")
    print(f"Verdict: [{verdict}] {message}")


def _print_audit_report(label, total_n, method, method_note,
                         first_verdict, first_score,
                         second_verdict, second_score,
                         second_n):
    """Prints a boxed audit summary report."""
    width = 64

    def pad(text):
        # Ensure consistent width inside the box
        return text + " " * max(0, width - 4 - len(text))

    top =    f"\n{'':>2}+{'=' * (width - 2)}+"
    bottom = f"{'':>2}+{'=' * (width - 2)}+"
    sep =    f"{'':>2}+{'-' * (width - 2)}+"
    blank =  f"{'':>2}| {pad('')} |"

    def row(text):
        return f"{'':>2}| {pad(text)} |"

    # Build method description
    method_desc = _method_display_name(method)
    if method_note:
        method_desc += f" ({method_note})"

    # First-digit score text
    if method == "chi2":
        first_detail = f"chi2 = {first_score:.2f}"
    else:
        first_detail = f"MAD = {first_score:.2f}"

    # Second-digit score text
    if second_n > 0:
        if method == "chi2":
            second_detail = f"chi2 = {second_score:.2f}"
        else:
            second_detail = f"MAD = {second_score:.2f}"
    else:
        second_detail = "skipped (insufficient data)"
        second_verdict = "N/A"

    # Overall verdict
    if first_verdict == "DEVIATION" or second_verdict == "DEVIATION":
        overall = "!! SUSPICIOUS -- review flagged digits"
        overall_symbol = "!!"
    else:
        overall = "CLEAN -- data appears natural"
        overall_symbol = "OK"

    # Recommendation
    if overall_symbol == "!!":
        recommendation = "Manual review of leading-digit anomalies recommended"
    else:
        recommendation = "No immediate action required"

    print(top)
    title_text = "AUDIT SUMMARY REPORT"
    title_pad_l = (width - 2 - len(title_text)) // 2
    title_pad_r = width - 2 - len(title_text) - title_pad_l
    print(f"{'':>2}|{' ' * title_pad_l}{title_text}{' ' * title_pad_r}|")
    print(sep)
    print(row(f"Dataset:        {label}"))
    print(row(f"Sample Size:    {total_n}"))
    print(row(f"Method:         {method_desc}"))
    print(blank)
    print(row(f"First-Digit:    {first_verdict:<12}({first_detail})"))
    print(row(f"Second-Digit:   {second_verdict:<12}({second_detail})"))
    print(blank)
    print(row(f"Overall:        [{overall_symbol}] {overall}"))
    print(row(f"Recommendation: {recommendation}"))
    print(bottom)


def run_analysis(values, requested_method, verbose, label):
    # --- First-digit analysis ---
    digits = extract_all_digits(values)
    n = len(digits)

    if n < 30:
        print("Warning: sample size is small (<30). Results may be unreliable.\n")

    method, method_note = _resolve_method(requested_method, n)
    if method_note:
        print(f"  {method_note}\n")

    expected_pct = benford_expected()
    counts, observed_pct = observed_distribution(digits)

    first_score, first_verdict, first_msg = _score_and_verdict(
        counts, observed_pct, expected_pct, n, method
    )

    _print_result_block(
        f"Benford's Law Analysis: {label}",
        n, method, first_score, first_verdict, first_msg,
    )

    if verbose:
        render_chart(observed_pct, expected_pct,
                     title="First-Digit Distribution")

    # --- Second-digit analysis ---
    digits2 = extract_all_second_digits(values)
    n2 = len(digits2)

    second_score, second_verdict, second_msg = 0.0, "N/A", ""

    if n2 >= 10:  # need a minimum to be meaningful
        expected_pct2 = benford_expected_second_digit()
        counts2, observed_pct2 = observed_distribution_second_digit(digits2)

        # Re-resolve method for second-digit
        method2, method_note2 = _resolve_method(requested_method, n2)

        second_score, second_verdict, second_msg = _score_and_verdict(
            counts2, observed_pct2, expected_pct2, n2, method2
        )

        _print_result_block(
            f"Second-Digit Benford Analysis: {label}",
            n2, method2, second_score, second_verdict, second_msg,
        )

        if verbose:
            render_chart(observed_pct2, expected_pct2,
                         digit_range=range(0, 10),
                         title="Second-Digit Distribution")
    else:
        print(f"\n  Second-digit test skipped: not enough multi-digit values "
              f"(n={n2}, need >= 10).")

    # --- Audit report ---
    short_method_note = ""
    if method_note:
        short_method_note = method_note.split("(")[0].strip() if "(" in method_note else method_note

    _print_audit_report(
        label, n, method, short_method_note,
        first_verdict, first_score,
        second_verdict, second_score,
        n2,
    )


def main():
    print(f"=== Benford Fraud Detector Tool ===".center(140))
    print(f"USER GUIDE: #: Visual difference b/t Expected vs Observed (longer bar = higher %).".center(140))
    print(f"Flagged: Digits showing greater mismatch.".center(140))
    print(f"Result: Based on comparing the avg deviation score to a fixed threshold.".center(140))
    parser = argparse.ArgumentParser(
        description="Detect anomalies in numeric data using Benford's Law."
    )
    parser.add_argument("--file", help="Path to a CSV file to analyze")
    parser.add_argument("--column", help="Column name to analyze (required with --file)")
    parser.add_argument(
        "--generate",
        choices=["natural", "random"],
        help="Generate synthetic demo data instead of reading a file",
    )
    parser.add_argument(
        "--test",
        choices=["mad", "chi2", "auto"],
        default="auto",
        help="Scoring method: 'mad', 'chi2', or 'auto' (default). "
             "Auto picks chi-square when n >= 50, else MAD.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show full digit-by-digit ASCII chart"
    )

    args = parser.parse_args()

    if args.generate:
        if args.generate == "natural":
            values = generate_natural_data()
            label = "Synthetic Natural Data"
        else:
            values = generate_random_data()
            label = "Synthetic Uniform Random Data"
        run_analysis(values, args.test, True, label)  # always show chart for demos

    elif args.file:
        if not args.column:
            print("Error: --column is required when using --file")
            sys.exit(1)
        values = load_from_csv(args.file, args.column)
        run_analysis(values, args.test, args.verbose, args.file)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
