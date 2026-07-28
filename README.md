# Benford's Law Fraud Detector

A command-line tool that checks whether a set of numbers looks "natural" or
"tampered" using a real math trick used in fraud audits: **Benford's Law**.

## What It Does

In most real-world data (populations, prices, expenses), numbers starting
with **1** show up far more often than numbers starting with **9**. This
tool checks if your data follows that natural pattern. Following the law which predicts
accurately that the leading digit is likely to be small.

## Requirements

- Python  installed on your computer (check with `python --version`)
- No installation needed — no extra packages required

## Setup

1. Unzip the folder you downloaded.
2. Open a terminal and go into the folder:
   ```
   cd benford_detector
   ```

## How to Run It

Copy-paste any of these commands:

### 1. See a "natural" example (this should PASS)
```
python main.py --generate natural
```

### 2. See a "fake/random" example (this should FAIL)
```
python main.py --generate random --test chi2
```

### 3. Test real data (world population by country)
```
python main.py --file sample_data/world_populations.csv --column population --verbose
```

### 4. Test tampered data (fake expense report)
```
python main.py --file sample_data/tampered_expenses.csv --column amount --verbose --test chi2
```

> If `python` doesn't work, try `python3` instead.

## Testing Your Own Data

1. Put your numbers in a CSV file with a column header (e.g. `amount`).
2. Run:
   ```
   python main.py --file yourfile.csv --column amount --verbose
   ```

## Reading the Output

```
Sample size: 1000              → how many numbers were checked
Method: Mean absolute deviation → which math test was used
Score: 0.62                     → how far off the data is from natural (lower = better)
Verdict: [MATCH]                → final result: MATCH or DEVIATION
```

**MATCH** = data looks natural.
**DEVIATION** = data looks unnatural / possibly manipulated.

## Understanding the Chart (only shown with `--verbose`)

```
Digit 1:  Expected 30.1%   Observed 28.4%
          E:########################
          O:######################
```

- **Expected** = what Benford's Law predicts for that digit
- **Observed** = what your actual data shows
- **`#` symbols** = just a visual bar; more `#` = higher percentage
- **`<-- flagged`** = this digit's observed % is off from expected by more
  than 5 points — worth a closer look

## Two Testing Methods

| Flag | Method | When it's used |
|---|---|---|
| *(default, no flag needed)* | Mean Absolute Deviation (MAD) | Quick, simple check |
| `--test chi2` | Chi-Square Test | Stricter, more statistically formal |

You choose the method or the tool picks automatically (based on sample size)

## Important Note

This tool gives a **heuristic**, not proof. Some real, honest data can still
deviate from Benford's Law (e.g. data with a narrow range or artificial
caps). Treat a "DEVIATION" result as a signal to investigate further, not
as confirmed fraud.
