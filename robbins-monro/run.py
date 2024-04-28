import argparse
import csv
from pathlib import Path

import numpy as np


################# Manual setup ##################

target_value = 0.0   # α
true_solution = 0.0  # θ


def true_func(x: float) -> float:
    return x + 2.0 * np.sin(x)


def noise(x: float) -> float:
    sigma = 1.0
    return np.random.normal(loc=0.0, scale=sigma)

#################################################


def observe(x: float) -> float:
    return true_func(x) + noise(x)


def robbins_monro(n_steps: int, step_coef: float, step_power: float) -> list[float]:
    """
    Compute a sample path until `n_steps` steps by the Robbins-Monro algorithm.
    The n-th step size a_n is defined by a_n = c / n^p, where c = `step_coef` and p = `step_power`.
    """
    x = np.random.uniform(low=-10.0, high=10.0)
    path = [x]
    for i in range(1, n_steps):
        a = step_coef / i**step_power
        y = observe(x)
        x += a * (target_value - y)
        path.append(x)
    return path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n_steps', type=int, help='Number of steps')
    parser.add_argument('output_path', type=Path, help='Output CSV path')
    parser.add_argument('-c', '--step-coef', type=float, default=1.0,
                        help='Coefficient in the step size (Default: 1.0)')
    parser.add_argument('-p', '--step-power', type=float, default=1.0,
                        help='Exponent in the step size (Default: 1.0)')
    parser.add_argument('-s', '--seed', type=int, default=42,
                        help='Seed of RNG (Default: 42)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n_steps: int = args.n_steps
    output_path: Path = args.output_path
    step_coef: float = args.step_coef
    step_power: float = args.step_power
    seed: int = args.seed
    assert n_steps >= 0, f'n_steps {n_steps} must be non-negative'

    np.random.seed(seed)

    result = robbins_monro(n_steps, step_coef, step_power)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['step', 'value', 'error'])
        writer.writeheader()
        writer.writerows([{'step': i + 1, 'value': x, 'error': np.abs(x - true_solution)}
                          for i, x in enumerate(result)])


if __name__ == '__main__':
    main()
