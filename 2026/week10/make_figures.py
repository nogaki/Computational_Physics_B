"""Reproduce the numerical ODE figures used in the lecture."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc


OUT = Path(__file__).parent / "figures"


def euler(f, x, t, h):
    return x + h * f(x, t)


def rk2(f, x, t, h):
    k1 = h * f(x, t)
    k2 = h * f(x + k1 / 2, t + h / 2)
    return x + k2


def rk4(f, x, t, h):
    k1 = h * f(x, t)
    k2 = h * f(x + k1 / 2, t + h / 2)
    k3 = h * f(x + k2 / 2, t + h / 2)
    k4 = h * f(x + k3, t + h)
    return x + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def integrate(step, f, x0, t0, h, nsteps):
    t = t0 + h * np.arange(nsteps + 1)
    x = np.empty(nsteps + 1)
    x[0] = x0
    for n in range(nsteps):
        x[n + 1] = step(f, x[n], t[n], h)
    return t, x


def adaptive_rk4(f, x0, t0, t_end, h0, tol):
    t, x, h = float(t0), float(x0), h0
    ts, xs, steps = [t], [x], []
    while t < t_end:
        h = min(h, t_end - t)
        full = rk4(f, x, t, h)
        half = rk4(f, rk4(f, x, t, h / 2), t + h / 2, h / 2)
        error = abs(half - full) / 15
        if not np.isfinite(error) or not np.isfinite(h):
            raise RuntimeError("non-finite RK4 step; reduce initial step size h0")
        factor = 2.0 if error == 0 else np.clip(
            0.9 * (tol / error) ** 0.2, 0.2, 2.0
        )
        if error <= tol:
            t += h
            x = half
            ts.append(t)
            xs.append(x)
            steps.append(h)
        h *= factor
        if t < t_end and h <= np.finfo(float).eps * max(1, abs(t)):
            raise RuntimeError("step size underflow")
    return np.asarray(ts), np.asarray(xs), np.asarray(steps)


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)

    def f(x, t):
        return -x**3 + np.sin(t)

    tref, xref = integrate(rk4, f, 0.0, 0.0, 10 / 2000, 2000)
    fig, ax = plt.subplots(figsize=(7.0, 3.8), constrained_layout=True)
    ax.plot(tref, xref, label="RK4 reference, N=2000")
    for name, method in (("Euler", euler), ("RK2", rk2), ("RK4", rk4)):
        t, x = integrate(method, f, 0.0, 0.0, 10 / 15, 15)
        ax.plot(t, x, "o", ms=3.5, label=f"{name}, N=15")
    ax.set(xlabel="t", ylabel="x(t)", title=r"$dx/dt=-x^3+\sin t$, $x(0)=0$")
    ax.legend(frameon=False, ncol=2)
    ax.grid(alpha=0.2)
    save(fig, "ode_methods.pdf")

    exact = np.exp(-1)
    hs = np.array([1 / 10, 1 / 20, 1 / 40, 1 / 80])
    fig, ax = plt.subplots(figsize=(6.5, 3.8), constrained_layout=True)
    for name, method in (("Euler", euler), ("RK2 midpoint", rk2), ("RK4", rk4)):
        errors = []
        for h in hs:
            _, x = integrate(method, lambda x, t: -x, 1.0, 0.0, h, round(1 / h))
            errors.append(abs(x[-1] - exact))
        ax.loglog(hs, errors, "o-", label=name)
    ax.set(xlabel="step size h", ylabel="absolute error at t=1")
    ax.legend(frameon=False)
    ax.grid(which="both", alpha=0.2)
    save(fig, "ode_order.pdf")

    c = 15.0

    def stiff(x, t):
        return -c * x

    t_exact = np.linspace(0, 1, 300)
    x_exact = np.exp(-c * t_exact)
    methods = (
        ("Euler", euler, "stiff_euler.pdf"),
        ("RK4", rk4, "stiff_rk4.pdf"),
    )
    for name, method, filename in methods:
        fig, ax = plt.subplots(figsize=(6.7, 3.8), constrained_layout=True)
        for h in (1 / 4, 1 / 8, 1 / 16):
            t, x = integrate(method, stiff, 1.0, 0.0, h, round(1 / h))
            ax.plot(t, x, "o-", ms=3, label=f"{name}, h={h:g}")
        ax.plot(t_exact, x_exact, "k--", label="exact")
        ax.set(xlabel="t", ylabel="x(t)", title=r"$dx/dt=-15x$, $x(0)=1$")
        ax.legend(frameon=False, ncol=2)
        ax.grid(alpha=0.2)
        save(fig, filename)

    fig, ax = plt.subplots(figsize=(6.7, 3.8), constrained_layout=True)
    for h in (1 / 4, 1 / 8, 1 / 16):
        t = h * np.arange(round(1 / h) + 1)
        x = np.empty_like(t)
        x[0] = 1.0
        for n in range(len(t) - 1):
            x[n + 1] = x[n] / (1 + c * h)
        ax.plot(t, x, "o-", ms=3, label=f"backward Euler, h={h:g}")
    ax.plot(t_exact, x_exact, "k--", label="exact")
    ax.set(xlabel="t", ylabel="x(t)", title=r"$dx/dt=-15x$, $x(0)=1$")
    ax.legend(frameon=False, ncol=2)
    ax.grid(alpha=0.2)
    save(fig, "stiff_backward.pdf")

    ta, xa, steps = adaptive_rk4(f, 0.0, 0.0, 10.0, 1.0, 1e-5)
    assert np.isfinite(ta).all() and ta[-1] == 10.0
    with np.errstate(over="ignore", invalid="ignore"):
        try:
            adaptive_rk4(f, 1.0, 0.0, 10.0, 10.0, 1e-5)
        except RuntimeError as exc:
            assert "reduce initial step size" in str(exc)
        else:
            raise AssertionError("non-finite adaptive step did not stop")
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.8), constrained_layout=True)
    axes[0].plot(tref, xref, label="RK4 reference, N=2000")
    axes[0].plot(ta, xa, "o", ms=3, label="accepted adaptive steps")
    axes[0].set(xlabel="t", ylabel="x(t)")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.2)
    axes[1].plot(ta[1:], steps, "o-", ms=3)
    axes[1].set(xlabel="t", ylabel="accepted step size h")
    axes[1].grid(alpha=0.2)
    fig.suptitle(r"RK4 step doubling, absolute tolerance $10^{-5}$")
    save(fig, "adaptive_rk4.pdf")

    fig, ax = plt.subplots(figsize=(4.5, 3.6), constrained_layout=True)
    theta = np.deg2rad(35)
    bob = np.array([np.sin(theta), -np.cos(theta)])
    ax.plot([-0.45, 0.45], [0.12, 0.12], color="0.2", lw=2)
    ax.plot([0, bob[0]], [0, bob[1]], color="#245a9b", lw=2)
    ax.scatter([0, bob[0]], [0, bob[1]], s=[20, 90], color=["black", "#c53b3b"])
    ax.plot([0, 0], [0, -1.1], "--", color="0.5", lw=1)
    ax.add_patch(Arc((0, 0), 0.55, 0.55, theta1=270, theta2=305, color="#d17a00"))
    ax.annotate(r"$\theta$", (0.12, -0.27), color="#d17a00")
    ax.annotate(r"$L$", (bob[0] / 2 - 0.07, bob[1] / 2))
    ax.annotate(r"$mg$", bob + np.array([0.1, -0.2]), color="#c53b3b")
    ax.set(xlim=(-0.6, 0.8), ylim=(-1.25, 0.3), xlabel="x/L", ylabel="y/L")
    ax.set_aspect("equal")
    ax.set_title("Simple pendulum")
    ax.grid(alpha=0.15)
    save(fig, "pendulum_scheme.pdf")


if __name__ == "__main__":
    main()
