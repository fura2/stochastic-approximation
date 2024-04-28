import argparse
import csv
from pathlib import Path
from typing import Optional

import matplotlib.pylab as plt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_paths', nargs='+', help='CSV paths')
    parser.add_argument('-a', '--alpha', type=float,
                        default=1.0, help='Alpha value')
    parser.add_argument('-o', '--output-path', type=Path,
                        help='Output image path')
    parser.add_argument('-d', '--dpi', type=float, default=200.0,
                        help='Output image DPI (Default: 200)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_paths: list = args.csv_paths
    alpha: float = args.alpha
    output_path: Optional[Path] = args.output_path
    dpi: float = args.dpi

    for i, path in enumerate(csv_paths):
        path = Path(path)
        with path.open('r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        xs = [int(row['step']) for row in rows]
        ys = [float(row['error']) for row in rows]
        plt.plot(xs, ys, linewidth=0.5, alpha=alpha, label=f'sample {i+1}')

    plt.xlim(left=1)
    plt.xlabel('Step')
    plt.ylabel('Error')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()

    if output_path is None:
        plt.show()
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=dpi)


if __name__ == '__main__':
    main()
