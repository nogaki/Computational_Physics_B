from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded
from scipy.sparse import diags, eye
from scipy.sparse.linalg import splu

plt.rcParams["font.family"] = "Noto Sans CJK JP"
OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)


def lap(u):
    return u[2:] - 2 * u[1:-1] + u[:-2]


def tridiagonal(diagonal, off, rhs):
    ab = np.zeros((3, len(diagonal)), dtype=np.result_type(diagonal, rhs))
    ab[0, 1:] = off
    ab[1] = diagonal
    ab[2, :-1] = off
    return solve_banded((1, 1), ab, rhs)


def wave_step(phi, psi, h, r, method):
    n = len(phi) - 2
    phinew, psinew = phi.copy(), psi.copy()
    if method == "FTCS":
        phinew[1:-1] = phi[1:-1] + h * psi[1:-1]
        psinew[1:-1] = psi[1:-1] + r * lap(phi)
    elif method == "陰解法":
        diagonal = np.full(n, 1 + 2 * r * h)
        off = np.full(n - 1, -r * h)
        psinew[1:-1] = tridiagonal(diagonal, off, psi[1:-1] + r * lap(phi))
        phinew[1:-1] = phi[1:-1] + h * psinew[1:-1]
    else:
        diagonal = np.full(n, 4 + 2 * r * h)
        off = np.full(n - 1, -r * h)
        rhs = 4 * psi[1:-1] + 4 * r * lap(phi) + r * h * lap(psi)
        psinew[1:-1] = tridiagonal(diagonal, off, rhs)
        phinew[1:-1] = phi[1:-1] + (h / 2) * (psinew[1:-1] + psi[1:-1])
    return phinew, psinew


def wave_energy(phi, psi, dx, speed):
    kinetic = dx * np.sum(psi[1:-1] ** 2) / 2
    gradient = speed**2 * np.sum(np.diff(phi) ** 2) / (2 * dx)
    return kinetic + gradient


length, points, speed, dt, mode = 1.0, 100, 0.1, 0.01, 40
x = np.linspace(0, length, points + 1)
dx = length / points
r = dt * speed**2 / dx**2
phi0 = np.sin(mode * np.pi * x / length)
psi0 = np.zeros_like(x)
energy0 = wave_energy(phi0, psi0, dx, speed)
time = np.arange(101) * dt
fig, ax = plt.subplots(figsize=(6.3, 4.4), constrained_layout=True)
styles = {"FTCS": ("#C43C39", "-"), "陰解法": ("#2878B5", "--"), "Crank--Nicolson": ("#299447", "-.")}
for method, (color, style) in styles.items():
    phi, psi = phi0.copy(), psi0.copy()
    ratio = [1.0]
    for _ in time[1:]:
        phi, psi = wave_step(phi, psi, dt, r, method)
        ratio.append(wave_energy(phi, psi, dx, speed) / energy0)
    ax.plot(time, ratio, color=color, linestyle=style, label=method)
    if not np.isfinite(ratio).all():
        raise RuntimeError(f"non-finite wave energy for {method}")
ax.set(xlabel="time", ylabel="$E(t)/E(0)$", title="固定端波動方程式：離散エネルギー")
ax.set_ylim(0, 4.5)
ax.grid(alpha=0.25)
ax.legend()
fig.savefig(OUT / "wave_energy.pdf")
plt.close(fig)


def scattering():
    length, points = 80.0, 3200
    x = np.linspace(-length / 2, length / 2, points + 1)
    dx, dt = x[1] - x[0], 0.004
    x0, sigma, k0 = -10.0, 1.8, 10.0
    height, width = 36.2, 0.5
    potential = np.zeros_like(x)
    potential[np.abs(x) <= width / 2] = height
    psi = (np.pi * sigma**2) ** (-0.25) * np.exp(
        -(x - x0) ** 2 / (2 * sigma**2) + 1j * k0 * (x - x0)
    )
    psi /= np.sqrt(np.trapezoid(np.abs(psi) ** 2, x))
    size = points - 1
    hamiltonian = diags(
        [-0.5 / dx**2 * np.ones(size - 1), 1 / dx**2 + potential[1:-1],
         -0.5 / dx**2 * np.ones(size - 1)], [-1, 0, 1], format="csc"
    )
    left = eye(size, format="csc") + 0.5j * dt * hamiltonian
    right = eye(size, format="csc") - 0.5j * dt * hamiltonian
    factor = splu(left)
    psi_t = psi[1:-1].copy()
    snapshots = {0.0: np.r_[0j, psi_t, 0j]}
    marks = {int(round(t / dt)): t for t in (0.8, 1.6, 2.4, 2.8)}
    for step in range(1, max(marks) + 1):
        psi_t = factor.solve(right @ psi_t)
        if step in marks:
            snapshots[marks[step]] = np.r_[0j, psi_t, 0j]
    density = np.abs(snapshots[2.8]) ** 2
    norm = np.trapezoid(density, x)
    reflected = np.trapezoid(density[x < 0], x[x < 0])
    transmitted = np.trapezoid(density[x > 0], x[x > 0])
    inside = np.abs(x) <= width / 2
    barrier_probability = np.trapezoid(density[inside], x[inside])
    if abs(norm - 1) > 1e-10:
        raise RuntimeError(f"Crank--Nicolson norm drift: {norm:g}")
    return x, potential, snapshots, norm, reflected, transmitted, barrier_probability


x, potential, snapshots, norm, reflected, transmitted, barrier_probability = scattering()
fig, ax = plt.subplots(figsize=(7.0, 4.5), constrained_layout=True)
for t, style in zip((0.0, 1.6, 2.4, 2.8), ("--", "-", "-.", ":")):
    ax.plot(x, np.abs(snapshots[t]) ** 2, linestyle=style, label=f"t={t:g} a.u.")
ax.fill_between(x, 0, potential / 160, color="gray", alpha=0.35, label="barrier / 160")
ax.set(xlim=(-35, 35), xlabel="$x$ [Bohr radius]", ylabel="$|\\psi(x,t)|^2$ [Bohr$^{-1}$]",
       title="ガウス波束のポテンシャル散乱")
ax.grid(alpha=0.2)
ax.legend(ncol=2, fontsize=8)
fig.savefig(OUT / "wave_packet_scattering.pdf")
plt.close(fig)
print(f"norm={norm:.12f}, reflection={reflected:.6f}, transmission={transmitted:.6f}, barrier={barrier_probability:.2e}")
