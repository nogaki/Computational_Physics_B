"""Extract executed notebook plots and create the two method schematics."""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import numpy as np


ROOT = Path(__file__).parent
FIGURES = ROOT / "figures"
PLOTS = (
    ("Lorenz.ipynb", "ax.plot(x, y, z", "lorenz_attractor.png"),
    ("Lorenz.ipynb", "plt.semilogy(time_points", "lorenz_sensitivity.png"),
    ("DoublePendulum.ipynb", "plt.plot(p1[:, 0]", "double_pendulum_trace.png"),
    ("MolecularDynamics.ipynb", "plt.plot(times, kinetic_per_particle", "md_energy.png"),
    ("MolecularDynamics.ipynb", "plt.plot(times, temperatures", "md_temperature.png"),
    ("MolecularDynamics.ipynb", "plt.plot(times, compressibility_factor", "md_pressure.png"),
    ("MolecularDynamics.ipynb", "initial_speeds =", "md_speed_distribution.png"),
)


def extract_notebook_plots():
    for notebook_name, marker, image_name in PLOTS:
        notebook = nbformat.read(ROOT / notebook_name, as_version=4)
        cell = next(
            (c for c in notebook.cells
             if c.cell_type == "code" and marker in c.source),
            None,
        )
        if cell is None:
            raise ValueError(f"missing plot cell: {notebook_name}: {marker}")
        image = next(
            (o.data["image/png"] for o in cell.outputs
             if "image/png" in o.get("data", {})),
            None,
        )
        if image is None:
            raise ValueError(
                f"run the plot cell in {notebook_name} before extracting figures"
            )
        (FIGURES / image_name).write_bytes(base64.b64decode(image))


def make_lj_potential():
    r = np.linspace(0.85, 3.5, 600)
    q6 = r**-6
    potential = 4 * (q6**2 - q6)
    r_min = 2**(1 / 6)
    fig, ax = plt.subplots(figsize=(6.5, 3.8), constrained_layout=True)
    ax.plot(r, potential, color="#245a9b")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.scatter([r_min], [-1], color="#c53b3b", zorder=3)
    ax.annotate(r"$r_m=2^{1/6}\sigma$, $V=-\epsilon$",
                (r_min, -1), xytext=(1.45, -0.62),
                arrowprops={"arrowstyle": "->", "lw": 0.8})
    ax.set(xlabel=r"reduced separation $r/\sigma$",
           ylabel=r"reduced potential $V/\epsilon$",
           title="Lennard--Jones pair potential")
    ax.set_ylim(-1.2, 3)
    ax.grid(alpha=0.2)
    fig.savefig(FIGURES / "lj_potential.pdf")
    plt.close(fig)


def make_leapfrog_diagram():
    fig, ax = plt.subplots(figsize=(7, 2.8), constrained_layout=True)
    x_times = np.arange(4)
    v_times = np.arange(-0.5, 3, 1)
    ax.scatter(x_times, np.ones_like(x_times), s=55,
               color="#245a9b", label=r"position $x_n$")
    ax.scatter(v_times, np.zeros_like(v_times), s=55,
               color="#c53b3b", label=r"velocity $v_{n+1/2}$")
    for n in range(3):
        ax.annotate("", xy=(n + 0.5, 0.12), xytext=(n, 0.88),
                    arrowprops={"arrowstyle": "->", "color": "0.45"})
        ax.annotate("", xy=(n + 1, 0.88), xytext=(n + 0.5, 0.12),
                    arrowprops={"arrowstyle": "->", "color": "0.45"})
    ax.set_xticks(x_times, [r"$t_n$", r"$t_{n+1}$", r"$t_{n+2}$", r"$t_{n+3}$"])
    ax.set_yticks([0, 1], [r"$v$ at half steps", r"$x$ at full steps"])
    ax.set_xlim(-0.7, 3.4)
    ax.set_ylim(-0.35, 1.35)
    ax.legend(loc="upper right", frameon=False, ncol=2)
    ax.set_title("Leapfrog stores position and velocity at staggered times")
    ax.grid(axis="x", alpha=0.15)
    fig.savefig(FIGURES / "leapfrog_timing.pdf")
    plt.close(fig)


def main():
    FIGURES.mkdir(exist_ok=True)
    extract_notebook_plots()
    make_lj_potential()
    make_leapfrog_diagram()


if __name__ == "__main__":
    main()
