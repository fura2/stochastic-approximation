import argparse
import csv
from pathlib import Path

import numpy as np


################# Manual setup ##################

true_solution = 0.0  # θ


def true_func(x: float) -> float:
    return -np.abs(x)


def noise(x: float) -> float:
    sigma = 1.0
    return np.random.normal(loc=0.0, scale=sigma)

#################################################


def observe(x: float) -> float:
    return true_func(x) + noise(x)


def kiefer_wolfowitz(n_steps: int, step_coef_a: float, step_power_a: float,
                     step_coef_c: float, step_power_c: float) -> list[float]:
    """
    Compute a sample path until `n_steps` steps by the Kiefer-Wolfowitz algorithm.
    The n-th step sizes a_n and c_n is defined by
      a_n = d / n^p and c_n = e / n^q,
    where d = `step_coef_a`, p = `step_power_a`, e = `step_coef_c`, q = `step_power_c`.
    """
    x = np.random.uniform(low=-10.0, high=10.0)
    path = [x]
    for i in range(1, n_steps):
        a = step_coef_a / i**step_power_a
        c = step_coef_c / i**step_power_c
        y1 = observe(x + c)
        y2 = observe(x - c)
        x += a * (y1 - y2) / c
        path.append(x)
    return path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n_steps', type=int, help='Number of steps')
    parser.add_argument('output_path', type=Path, help='Output CSV path')
    parser.add_argument('-c', '--step-coef-a', type=float, default=1.0,
                        help='Coefficient in the step size a_n (Default: 1.0)')
    parser.add_argument('-p', '--step-power-a', type=float, default=1.0,
                        help='Exponent in the step size a_n (Default: 1.0)')
    parser.add_argument('-C', '--step-coef-c', type=float, default=1.0,
                        help='Coefficient in the step size c_n (Default: 1.0)')
    parser.add_argument('-P', '--step-power-c', type=float, default=1/3,
                        help='Exponent in the step size c_n (Default: 1/3)')
    parser.add_argument('-s', '--seed', type=int, default=42,
                        help='Seed of RNG (Default: 42)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n_steps: int = args.n_steps
    output_path: Path = args.output_path
    step_coef_a: float = args.step_coef_a
    step_power_a: float = args.step_power_a
    step_coef_c: float = args.step_coef_c
    step_power_c: float = args.step_power_c
    seed: int = args.seed
    assert n_steps >= 0, f'n_steps {n_steps} must be non-negative'

    np.random.seed(seed)

    result = kiefer_wolfowitz(n_steps, step_coef_a,
                              step_power_a, step_coef_c, step_power_c)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['step', 'value', 'error'])
        writer.writeheader()
        writer.writerows([{'step': i, 'value': x, 'error': np.abs(x - true_solution)}
                          for i, x in enumerate(result)])


if __name__ == '__main__':
    main()
