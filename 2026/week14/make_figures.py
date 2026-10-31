from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Noto Sans CJK JP"
OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)


def f(x):
    return x**3 - x - 2


def df(x):
    return 3 * x**2 - 1


def bisect_history(a, b, steps=28):
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError("the interval must contain a sign change")
    xs, errors = [], []
    for _ in range(steps):
        mid = a + (b - a) / 2
        fm = f(mid)
        xs.append(mid)
        errors.append(abs(fm))
        if fm == 0:
            break
        if (fa < 0) != (fm < 0):
            b, fb = mid, fm
        else:
            a, fa = mid, fm
    return xs, errors


def newton_history(x, steps=12):
    xs, errors = [x], [abs(f(x))]
    for _ in range(steps):
        x -= f(x) / df(x)
        xs.append(x)
        errors.append(abs(f(x)))
        if errors[-1] < 1e-14:
            break
    return xs, errors


def secant_history(x0, x1, steps=12):
    f0, f1 = f(x0), f(x1)
    xs, errors = [x0, x1], [abs(f0), abs(f1)]
    for _ in range(steps):
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = f(x2)
        xs.append(x2)
        errors.append(abs(f2))
        if abs(f2) < 1e-14:
            break
        x0, f0, x1, f1 = x1, f1, x2, f2
    return xs, errors


bisect_x, bisect_err = bisect_history(1.0, 2.0)
newton_x, newton_err = newton_history(1.5)
secant_x, secant_err = secant_history(1.0, 2.0)
assert abs(bisect_x[-1] - 1.5213797068) < 1e-7
assert abs(newton_x[-1] - 1.5213797068) < 1e-10
assert abs(secant_x[-1] - 1.5213797068) < 1e-10

root = newton_x[-1]
x0 = 1.3
x1 = x0 - f(x0) / df(x0)
x = np.linspace(0.85, 2.15, 500)
fig, ax = plt.subplots(figsize=(6.5, 4.4), constrained_layout=True)
ax.axvspan(1, 2, color="#4472C4", alpha=0.08, label="bisection bracket [1, 2]")
ax.plot(x, f(x), color="#2878B5", label="$f(x)=x^3-x-2$")
ax.plot(x, f(x0) + df(x0) * (x - x0), "--", color="#C43C39", label=fr"tangent at $x_0={x0:g}$")
ax.axhline(0, color="black", linewidth=0.8)
ax.scatter([x0, x1, root], [f(x0), 0, 0], color=["#C43C39", "#C43C39", "#299447"], zorder=3)
ax.annotate("$x_0$", (x0, f(x0)), xytext=(-14, -20), textcoords="offset points")
ax.annotate("Newton step", (x1, 0), xytext=(8, 14), textcoords="offset points")
ax.annotate("root", (root, 0), xytext=(8, -20), textcoords="offset points")
ax.set(xlabel="$x$", ylabel="$f(x)$", title="二分法の区間とNewton法の接線")
ax.set_ylim(-3.3, 4.5)
ax.grid(alpha=0.2)
ax.legend(fontsize=8)
fig.savefig(OUT / "root_geometry.pdf")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 4.4), constrained_layout=True)
ax.semilogy(range(len(bisect_err)), bisect_err, "o-", color="#C43C39", label="bisection")
ax.semilogy(range(len(newton_err)), newton_err, "s--", color="#2878B5", label="Newton")
ax.semilogy(range(len(secant_err)), secant_err, "^:", color="#299447", label="secant")
ax.set(xlabel="iteration", ylabel="$|f(x_n)|$", title="根の探索：残差の減少")
ax.grid(alpha=0.25, which="both")
ax.legend()
fig.savefig(OUT / "root_convergence.pdf")
plt.close(fig)
