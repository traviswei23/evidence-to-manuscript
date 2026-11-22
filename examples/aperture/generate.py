"""Recreate the illustrative radial quadrature, analytic check and figure (Matplotlib required)."""

import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def captured(radius, cells):
    step = radius / cells
    midpoints = ((i + 0.5) * step for i in range(cells))
    return step * sum(4 * r * math.exp(-2 * r * r) for r in midpoints)


def main():
    base = Path(__file__).resolve().parent
    radii = [0.25, 0.5, 1.0, 1.5]
    with (base / "results.csv").open("w", newline="", encoding="utf-8") as stream:
        out = csv.writer(stream, lineterminator="\n")
        out.writerow(["radius_over_w", "cells", "capture", "unit", "analytic"])
        for cells in (100, 200):
            for radius in radii:
                analytic = 100 * (1 - math.exp(-2 * radius ** 2))
                out.writerow([radius, cells, f"{100 * captured(radius, cells):.9f}", "%",
                              f"{analytic:.9f}"])
    x = [i / 100 for i in range(161)]
    fig, ax = plt.subplots(figsize=(5.1, 3.2), layout="constrained")
    ax.plot(x, [100 * (1 - math.exp(-2 * r * r)) for r in x], color="#313b45",
            label="Analytic integral")
    ax.scatter(radii, [100 * captured(r, 200) for r in radii], color="#136e75",
               label="Midpoint quadrature (200 cells)", zorder=3)
    ax.set(xlabel="Aperture radius / beam radius", ylabel="Collected power (%)",
           xlim=(0, 1.6), ylim=(0, 105))
    ax.legend(frameon=False)
    fig.savefig(base / "collection.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
