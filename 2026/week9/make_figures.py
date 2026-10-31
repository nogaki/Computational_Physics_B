"""Reproduce the figures used in the Ising Monte Carlo lecture."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).parent / "figures"
L = 20
J = 1.0
KB = 1.0


def attempt(spins, temperature, rng):
    i, j = rng.integers(L, size=2)
    neighbor_sum = (
        spins[(i - 1) % L, j] + spins[(i + 1) % L, j]
        + spins[i, (j - 1) % L] + spins[i, (j + 1) % L]
    )
    delta_e = 2 * J * spins[i, j] * neighbor_sum
    if delta_e <= 0 or rng.random() < np.exp(-delta_e / (KB * temperature)):
        spins[i, j] *= -1
        return True
    return False


def energy(spins):
    return -J * np.sum(
        spins * (np.roll(spins, -1, axis=0) + np.roll(spins, -1, axis=1))
    )


def main():
    OUT.mkdir(exist_ok=True)
    rng = np.random.default_rng(20261215)

    # Show coarsening from a random state at a low temperature.
    spins = rng.choice((-1, 1), size=(L, L))
    snapshots = [spins.copy()]
    for _ in range(3):
        for _ in range(30_000):
            attempt(spins, 1.8, rng)
        snapshots.append(spins.copy())
    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.2), constrained_layout=True)
    for ax, state, count in zip(axes.flat, snapshots, (0, 30_000, 60_000, 90_000)):
        ax.imshow(state, cmap="coolwarm", vmin=-1, vmax=1, interpolation="nearest")
        ax.set_title(f"{count:,} attempted flips")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle(r"$L=20$, $k_BT/J=1.8$; periodic boundaries")
    fig.savefig(OUT / "ising_snapshots.pdf")
    plt.close(fig)

    # The trace starts from the ordered state to show burn-in near Tc.
    spins = np.ones((L, L), dtype=np.int8)
    trace = []
    accepted = 0
    for n in range(200_000):
        accepted += attempt(spins, 2.2, rng)
        if (n + 1) % 100 == 0:
            trace.append(np.mean(spins))
    fig, ax = plt.subplots(figsize=(7.0, 3.4), constrained_layout=True)
    x = np.arange(100, 200_001, 100)
    ax.plot(x, np.abs(trace), lw=0.65, color="#245a9b")
    ax.axvline(30_000, color="0.45", ls="--", lw=0.9)
    ax.set_xlabel("attempted spin flips")
    ax.set_ylabel(r"$|m|=|N^{-1}\sum_i s_i|$")
    ax.set_title(rf"$L=20$, $k_BT/J=2.2$; acceptance={accepted/200_000:.2f}")
    ax.grid(alpha=0.2)
    fig.savefig(OUT / "magnetization_trace.pdf")
    plt.close(fig)

    # A short finite-size estimate; this is illustrative, not a precision result.
    temperatures = np.array([1.8, 2.0, 2.2, 2.4, 2.6, 2.8])
    estimate = []
    for temperature in temperatures:
        spins = np.ones((L, L), dtype=np.int8)
        values = []
        for n in range(300_000):
            attempt(spins, temperature, rng)
            if n >= 60_000 and (n + 1) % 1_200 == 0:
                values.append(abs(np.mean(spins)))
        estimate.append(np.mean(values))

    exact_t = np.linspace(1.0, 2.0 / np.log(1.0 + np.sqrt(2.0)), 200)
    exact_m = (1.0 - np.sinh(2.0 / exact_t) ** -4) ** (1.0 / 8.0)
    fig, ax = plt.subplots(figsize=(6.7, 3.8), constrained_layout=True)
    ax.plot(temperatures, estimate, "o", label=r"MC: $L=20$, $\langle|m|\rangle$")
    ax.plot(exact_t, exact_m, "-", label="2D exact, infinite lattice")
    ax.axvline(2.0 / np.log(1.0 + np.sqrt(2.0)), color="0.5", ls="--", lw=0.9)
    ax.set_xlabel(r"reduced temperature $k_BT/J$")
    ax.set_ylabel("magnetization per spin")
    ax.set_ylim(-0.03, 1.05)
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.savefig(OUT / "ising_magnetization.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
