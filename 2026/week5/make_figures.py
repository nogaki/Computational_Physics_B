"""Regenerate the figures used by the week 5 visualization notebook."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import jv


HERE = Path(__file__).resolve().parent
FIGURES = HERE / "figures"
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "legend.fontsize": 9,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


def save(fig, filename):
    fig.savefig(FIGURES / filename, bbox_inches="tight")
    plt.close(fig)


def cos_points(n):
    x = np.linspace(0, 10, n)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, np.cos(x), "o", color="C0")
    ax.set(xlabel="x [rad]", ylabel="cos(x)", xlim=(0, 10), ylim=(-1.15, 1.15))
    ax.grid(alpha=0.25)
    return fig


def cos_line():
    x = np.linspace(0, 10, 101)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, np.cos(x), color="C0", label="cos(x)")
    ax.set(xlabel="x [rad]", ylabel="cos(x)", xlim=(0, 10), ylim=(-1.15, 1.15))
    ax.legend()
    ax.grid(alpha=0.25)
    return fig


def multiple_lines():
    x = np.linspace(0, 10, 101)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, np.cos(x), "C0-", label="cos(x)")
    ax.plot(x, np.sin(x), "C1--", label="sin(x)")
    ax.set(xlabel="x [rad]", ylabel="Function value", xlim=(0, 10), ylim=(-1.15, 1.15))
    ax.legend()
    ax.grid(alpha=0.25)
    return fig


def bad_sampling():
    x = np.linspace(0, 10, 7)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, np.cos(x), "o-", color="C0")
    ax.set(title="Too few samples", xlabel="x [rad]", ylabel="cos(x)", xlim=(0, 10), ylim=(-1.15, 1.15))
    ax.grid(alpha=0.25)
    return fig


def bad_labels():
    x = np.linspace(0, 10, 101)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, np.cos(x), color="C0")
    # Deliberately omit axis labels to demonstrate an unreadable plot.
    return fig


def bad_styles():
    x = np.linspace(0, 10, 101)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, np.cos(x), "C0-", label="cos(x)")
    ax.plot(x, np.sin(x), "C0-", label="sin(x)")
    ax.set(xlabel="x [rad]", ylabel="Function value", xlim=(0, 10), ylim=(-1.15, 1.15))
    ax.legend()
    ax.grid(alpha=0.25)
    return fig


def scatter_example():
    rng = np.random.default_rng(2026)
    x = rng.normal(size=250)
    y = 1.4 * x + 0.65 * rng.normal(size=x.size)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.scatter(x, y, s=22, alpha=0.65, color="C0")
    ax.set(title="Synthetic correlated data (simulation)", xlabel="x [arbitrary units]", ylabel="y [arbitrary units]")
    ax.grid(alpha=0.25)
    return fig


def load_pulsars():
    raw = pd.read_csv(HERE / "pulsar.csv")
    values = raw[["P0", "P1"]].apply(pd.to_numeric, errors="coerce").to_numpy()
    valid = np.isfinite(values).all(axis=1) & (values > 0).all(axis=1)
    return raw.loc[valid].copy(), len(raw)


def pulsar_plot(data):
    period = data["P0"].to_numpy()
    period_dot = data["P1"].to_numpy()
    assert np.isfinite(period).all() and np.isfinite(period_dot).all()
    assert (period > 0).all() and (period_dot > 0).all()

    p_grid = np.logspace(-3, 2, 500)
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    ax.scatter(period, period_dot, s=10, alpha=0.2, color="C0", label="ATNF catalogue")

    for index, field in enumerate((1e8, 1e10, 1e12, 1e14)):
        pdot = (field / 3.2e19) ** 2 / p_grid
        ax.plot(p_grid, pdot, "--", color=plt.cm.Oranges(0.35 + 0.15 * index), label=f"B = {field:.0e} G")

    seconds_per_year = 365.25 * 24 * 60 * 60
    for index, age in enumerate((1e3, 1e6, 1e9)):
        pdot = p_grid / (2 * age * seconds_per_year)
        ax.plot(p_grid, pdot, ":", color=plt.cm.Greens(0.45 + 0.15 * index), label=rf"$τ_c$ = {age:.0e} yr")

    ax.set(xscale="log", yscale="log", xlim=(1e-3, 1e2), ylim=(1e-22, 1e-9),
           xlabel=r"Period $P$ [s]", ylabel=r"Period derivative $\dot{P}$ [s/s]",
           title=f"Pulsar period and period derivative (n={len(data):,})")
    ax.grid(True, which="both", alpha=0.2)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8, frameon=False)
    fig.subplots_adjust(right=0.73, bottom=0.18)
    fig.text(0.12, 0.025, "Source: ATNF Pulsar Catalogue. B and characteristic age are model estimates.", fontsize=8)
    return fig


def dipole_field():
    x = np.linspace(-5, 5, 200)
    y = np.linspace(-5, 5, 200)
    X, Y = np.meshgrid(x, y)
    r_plus = np.hypot(X + 2, Y)
    r_minus = np.hypot(X - 2, Y)
    outside = (r_plus >= 0.25) & (r_minus >= 0.25)
    positive = np.divide(1.0, r_plus, out=np.zeros_like(r_plus), where=r_plus >= 0.25)
    negative = np.divide(1.0, r_minus, out=np.zeros_like(r_minus), where=r_minus >= 0.25)
    potential = np.ma.masked_where(~outside, positive - negative)
    assert potential.shape == (200, 200)
    assert np.ma.getmaskarray(potential).any()
    return X, Y, potential


def dipole_contours():
    X, Y, potential = dipole_field()
    levels = np.linspace(-1.5, 1.5, 13)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.5), constrained_layout=True)
    lines = ax1.contour(X, Y, potential, levels=levels, colors="black", linewidths=0.8)
    ax1.clabel(lines, inline=True, fontsize=8, fmt="%.1f")
    ax1.set_title("Contour lines")
    filled = ax2.contourf(X, Y, potential, levels=levels, cmap="RdBu_r", extend="both")
    fig.colorbar(filled, ax=ax2, label="Dimensionless potential")
    ax2.set_title("Filled contours")
    for ax in (ax1, ax2):
        ax.set(xlabel="x", ylabel="y", xlim=(-5, 5), ylim=(-5, 5), aspect="equal")
        ax.plot(-2, 0, "k+", ms=9, mew=1.5)
        ax.plot(2, 0, "kx", ms=7, mew=1.5)
    return fig


def dipole_density():
    X, Y, potential = dipole_field()
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    image = ax.imshow(potential, origin="lower", extent=(-5, 5, -5, 5),
                      cmap="RdBu_r", vmin=-1.5, vmax=1.5, interpolation="nearest")
    fig.colorbar(image, ax=ax, label="Dimensionless potential")
    ax.plot(-2, 0, "k+", ms=9, mew=1.5)
    ax.plot(2, 0, "kx", ms=7, mew=1.5)
    ax.set(xlabel="x", ylabel="y", title="Dipole potential density", xlim=(-5, 5), ylim=(-5, 5), aspect="equal")
    return fig


def dipole_surface():
    X, Y, potential = dipole_field()
    fig = plt.figure(figsize=(8.0, 6.0), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, potential, rstride=3, cstride=3, cmap="RdBu_r",
                    vmin=-5, vmax=5, linewidth=0, antialiased=True)
    ax.contourf(X, Y, potential, zdir="z", offset=-5,
                levels=np.linspace(-1.5, 1.5, 13), cmap="RdBu_r", vmin=-1.5, vmax=1.5)
    ax.set(xlim=(-5, 5), ylim=(-5, 5), zlim=(-5, 5), xlabel="x", ylabel="y", zlabel="Potential")
    ax.set_title("Dipole potential surface with a base contour")
    ax.view_init(elev=28, azim=55)
    return fig


def bessel_plot():
    x = np.linspace(0, 20, 500)
    styles = ("-", "--", ":", "-.")
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for order, style in enumerate(styles):
        ax.plot(x, jv(order, x), linestyle=style, label=rf"$J_{order}(x)$")
    ax.set(xlabel="x", ylabel=r"$J_v(x)$", xlim=(0, 20), title="Bessel functions of the first kind")
    ax.legend(ncol=2)
    ax.grid(alpha=0.25)
    return fig


def mandelbrot_plot():
    width, height, max_iter = 1000, 750, 80
    real = np.linspace(-2.2, 0.8, width)
    imag = np.linspace(-1.5, 1.5, height)
    C = real[None, :] + 1j * imag[:, None]
    Z = np.zeros(C.shape, dtype=complex)
    active = np.ones(C.shape, dtype=bool)
    escape_iteration = np.zeros(C.shape, dtype=np.uint16)
    for iteration in range(1, max_iter + 1):
        Z[active] = Z[active] * Z[active] + C[active]
        escaped = active & (np.abs(Z) > 2)
        escape_iteration[escaped] = iteration
        active &= ~escaped
        if not active.any():
            break
    image_data = np.ma.masked_where(active, escape_iteration)
    fig, ax = plt.subplots(figsize=(8.0, 5.8))
    cmap = plt.colormaps["magma"].copy()
    cmap.set_bad("black")
    image = ax.imshow(image_data, origin="lower", extent=(-2.2, 0.8, -1.5, 1.5), cmap=cmap,
                      interpolation="nearest", vmin=1, vmax=max_iter)
    fig.colorbar(image, ax=ax, label="Escape iteration")
    ax.set(xlabel="Re(c)", ylabel="Im(c)", title=f"Mandelbrot set (escape-time approximation, {max_iter} iterations)")
    return fig


def generate_all():
    FIGURES.mkdir(exist_ok=True)
    for name, count in (("cos_points_11.pdf", 11), ("cos_points_101.pdf", 101)):
        x = np.linspace(0, 10, count)
        assert len(x) == count and x[0] == 0 and x[-1] == 10
        save(cos_points(count), name)
    save(cos_line(), "cos_line.pdf")
    save(multiple_lines(), "multiple_lines.pdf")
    save(bad_sampling(), "bad_sampling.pdf")
    save(bad_labels(), "bad_labels.pdf")
    save(bad_styles(), "bad_styles.pdf")
    save(scatter_example(), "scatter_example.pdf")

    data, total = load_pulsars()
    assert len(data) > 0 and len(data) <= total
    print(f"Pulsar rows: {len(data)} positive finite P0/P1 of {total} total")
    save(pulsar_plot(data), "pulsar.pdf")

    save(dipole_contours(), "dipole_contours.pdf")
    save(dipole_density(), "dipole_density.pdf")
    save(dipole_surface(), "dipole_surface.pdf")
    save(bessel_plot(), "bessel.pdf")
    save(mandelbrot_plot(), "mandelbrot.png")


if __name__ == "__main__":
    generate_all()
