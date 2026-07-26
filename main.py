#!/usr/bin/env python3
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

from digit_extractor import extract_all_digits
from distribution import benford_expected, observed_distribution
from scorer import mean_absolute_deviation, chi_square_statistic, get_verdict
from visualizer import render_chart
from data_generator import generate_natural_data, generate_random_data


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


def run_analysis(values, method, verbose, label):
    digits = extract_all_digits(values)

    if len(digits) < 30:
        print("Warning: sample size is small (<30). Results may be unreliable.\n")

    expected_pct = benford_expected()
    counts, observed_pct = observed_distribution(digits)

    if method == "chi2":
        score = chi_square_statistic(counts, expected_pct, len(digits))
    else:
        score = mean_absolute_deviation(observed_pct, expected_pct)

    verdict, message = get_verdict(score, method)

    print(f"\n=== Benford's Law Analysis: {label} ===")
    print(f"Sample size: {len(digits)}")
    print(f"Method: {'Chi-square goodness-of-fit' if method == 'chi2' else 'Mean absolute deviation'}")
    print(f"Score: {score:.2f}")
    print(f"Verdict: [{verdict}] {message}")

    if verbose:
        render_chart(observed_pct, expected_pct)


def main():
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
        choices=["mad", "chi2"],
        default="mad",
        help="Scoring method: 'mad' (mean absolute deviation, default) or 'chi2'",
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
