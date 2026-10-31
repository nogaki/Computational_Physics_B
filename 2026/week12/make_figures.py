from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

plt.rcParams["font.family"] = "Noto Sans CJK JP"


OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)


def laplace_field(n=40, omega=1.75, tol=1e-9):
    phi = np.zeros((n + 1, n + 1))
    phi[1:-1, -1] = 1.0
    for _ in range(20_000):
        delta = 0.0
        for i in range(1, n):
            for j in range(1, n):
                old = phi[i, j]
                average = 0.25 * (phi[i - 1, j] + phi[i + 1, j]
                                  + phi[i, j - 1] + phi[i, j + 1])
                phi[i, j] = old + omega * (average - old)
                delta = max(delta, abs(phi[i, j] - old))
        if delta < tol:
            break
    else:
        raise RuntimeError("SOR did not converge")
    return phi


def heat_step(u, r, method):
    n = len(u) - 1
    size = n - 1
    if method == "FTCS":
        out = u.copy()
        out[1:n] += r * (u[2:] - 2 * u[1:n] + u[:-2])
        return out
    if method == "陰解法":
        diagonal, off = np.full(size, 1 + 2 * r), np.full(size - 1, -r)
        rhs = u[1:n].copy()
        rhs[0] += r * u[0]
        rhs[-1] += r * u[n]
    else:
        diagonal, off = np.full(size, 1 + r), np.full(size - 1, -r / 2)
        rhs = (1 - r) * u[1:n] + (r / 2) * (u[:-2] + u[2:])
        rhs[0] += (r / 2) * u[0]
        rhs[-1] += (r / 2) * u[n]
    ab = np.zeros((3, size))
    ab[0, 1:] = off
    ab[1] = diagonal
    ab[2, :-1] = off
    out = u.copy()
    out[1:n] = solve_banded((1, 1), ab, rhs)
    return out


phi = laplace_field()
x = np.linspace(0, 1, len(phi))
xx, yy = np.meshgrid(x, x, indexing="ij")
fig, ax = plt.subplots(figsize=(6.3, 4.5), constrained_layout=True)
contour = ax.contourf(xx, yy, phi, levels=18, cmap="viridis")
ax.contour(xx, yy, phi, levels=9, colors="white", linewidths=0.45)
ax.set(xlabel="$x/L$", ylabel="$y/L$", title="Laplace 方程式：正方形領域の電位")
ax.set_aspect("equal")
fig.colorbar(contour, ax=ax, label="$\\phi/V$")
fig.savefig(OUT / "laplace_potential.pdf")
plt.close(fig)

length, diffusivity, n = 0.01, 4.25e-6, 40
dx = length / n
dt = 0.4 * dx**2 / diffusivity
r = diffusivity * dt / dx**2
u0 = np.full(n + 1, 20.0)
u0[0], u0[-1] = 50.0, 0.0
profiles = {}
for method in ("FTCS", "陰解法", "Crank--Nicolson"):
    u = u0.copy()
    for _ in range(round(1.0 / dt)):
        u = heat_step(u, r, method)
    profiles[method] = u

fig, ax = plt.subplots(figsize=(6.3, 4.5), constrained_layout=True)
for method, profile in profiles.items():
    ax.plot(np.linspace(0, length * 100, n + 1), profile, label=method)
ax.set(xlabel="$x$ [cm]", ylabel="$T$ [$^\\circ$C]", title="棒の温度分布：$t=1$ s")
ax.legend()
ax.grid(alpha=0.25)
fig.savefig(OUT / "heat_methods.pdf")
plt.close(fig)

theta = np.linspace(0, np.pi, 300)
fig, ax = plt.subplots(figsize=(6.3, 4.5), constrained_layout=True)
for rr in (0.4, 0.6):
    gain = 1 - 4 * rr * np.sin(theta / 2) ** 2
    ax.plot(theta / np.pi, np.abs(gain), label=fr"$r={rr}$")
ax.axhline(1, color="black", linewidth=0.8)
ax.set(xlabel="$k\\Delta x/\\pi$", ylabel="$|G|$", title="FTCS の増幅率")
ax.set_ylim(0, 1.55)
ax.legend()
ax.grid(alpha=0.25)
fig.savefig(OUT / "ftcs_stability.pdf")
plt.close(fig)
