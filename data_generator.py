"""Generates synthetic datasets to demonstrate Benford's Law passing/failing."""

import random


def generate_natural_data(n=1000):
    """
    Generates values that are uniform in LOG SPACE (spanning several
    orders of magnitude), which is the actual condition that produces
    a Benford-compliant leading-digit distribution. Mimics real-world
    scale-invariant quantities like populations or prices.
    """
    data = []
    for _ in range(n):
        exponent = random.uniform(1, 6)  # spans 10^1 to 10^6
        value = 10 ** exponent
        data.append(round(value, 2))
    return data


def generate_random_data(n=1000):
    """Uniformly distributed integers -- should NOT satisfy Benford's Law."""
    return [random.randint(1000, 9999) for _ in range(n)]


def generate_tampered_data(base_data, fraction=0.2):
    """
    Takes real/natural data and replaces a fraction of it with
    human-invented 'round-looking' numbers to simulate fraud.
    """
    tampered = list(base_data)
    n_replace = int(len(tampered) * fraction)
    fake_choices = [500, 1000, 1500, 2000, 2500, 5000, 7500, 9000, 9999]

    indices = random.sample(range(len(tampered)), min(n_replace, len(tampered)))
    for i in indices:
        tampered[i] = random.choice(fake_choices) + random.uniform(0, 1)

    return tampered
