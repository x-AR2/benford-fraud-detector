"""Renders side-by-side ASCII bar charts comparing observed vs expected distributions."""

BAR_CHAR = "#"
MAX_BAR_WIDTH = 40


def render_bar(pct):
    filled = int((pct / 100) * MAX_BAR_WIDTH * 2)  # scale for visibility
    return BAR_CHAR * filled


def render_chart(observed_pct, expected_pct, flag_threshold=5.0,
                 digit_range=None, title=None):
    """
    Prints a side-by-side ASCII chart of expected vs observed distributions.

    Both E: and O: bars start from the same column so visual mismatches
    are obvious at a glance.

    Parameters
    ----------
    digit_range : range, optional
        The range of digits to chart. Defaults to range(1, 10) for first-digit.
    title : str, optional
        An optional section title printed above the chart.
    """
    if digit_range is None:
        digit_range = range(1, 10)

    if title:
        print(f"\n  {title}")

    print(f"\n{'Digit':<7}{'Expected':<10}{'Observed':<10}Chart")
    print("-" * 70)
    for d in digit_range:
        exp = expected_pct[d]
        obs = observed_pct[d]
        flag = " <-- flagged" if abs(obs - exp) > flag_threshold else ""

        # Both E: and O: bars start at the same column (position 27)
        bar_prefix = f"  {d}    {exp:5.1f}%    {obs:5.1f}%   "
        spacer = " " * len(bar_prefix)

        print(f"{bar_prefix}E: {render_bar(exp)}")
        print(f"{spacer}O: {render_bar(obs)}{flag}")
    print("-" * 70)
