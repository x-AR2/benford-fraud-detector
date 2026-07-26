"""Renders side-by-side ASCII bar charts comparing observed vs expected distributions."""

BAR_CHAR = "#"
MAX_BAR_WIDTH = 40


def render_bar(pct):
    filled = int((pct / 100) * MAX_BAR_WIDTH * 2)  # scale for visibility
    return BAR_CHAR * filled


def render_chart(observed_pct, expected_pct, flag_threshold=5.0):
    print(f"\n{'Digit':<7}{'Expected':<10}{'Observed':<10}Chart")
    print("-" * 70)
    for d in range(1, 10):
        exp = expected_pct[d]
        obs = observed_pct[d]
        flag = " <-- flagged" if abs(obs - exp) > flag_threshold else ""

        print(f"  {d}    {exp:5.1f}%    {obs:5.1f}%   "
              f"E:{render_bar(exp)}")
        print(f"{'':17}O:{render_bar(obs)}{flag}")
    print("-" * 70)
