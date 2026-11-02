from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

out = Path(__file__).parent / "figures"
out.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.labelsize": 10, "axes.titlesize": 11})

def f(x):
    return x**4 - 2*x + 2

a, b, n = 0.0, 2.0, 4
h = (b - a) / n
x = np.linspace(a, b, 500)

fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.plot(x, f(x), color="#C0504D", label="$f(x)$")
for i in range(n):
    mid = a + (i + 0.5) * h
    ax.add_patch(Rectangle((a + i*h, 0), h, f(mid), facecolor="#8FAADC", edgecolor="#4472C4", alpha=.72))
ax.set(xlim=(a, b), xlabel="$x$", ylabel="$f(x)$", title="Composite midpoint rule ($N=4$)")
ax.legend(frameon=False)
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(out / "midpoint_rule.pdf")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.plot(x, f(x), color="#C0504D", label="$f(x)$")
for i in range(n):
    x0, x1 = a + i*h, a + (i+1)*h
    y0, y1 = f(x0), f(x1)
    ax.fill([x0, x0, x1, x1], [0, y0, y1, 0], color="#8FAADC", alpha=.55)
    ax.plot([x0, x1], [y0, y1], color="#4472C4", linewidth=1.5, label="linear interpolation" if i == 0 else None)
ax.set(xlim=(a, b), xlabel="$x$", ylabel="$f(x)$", title="Composite trapezoidal rule ($N=4$)")
ax.legend(frameon=False)
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(out / "trapezoid_rule.pdf")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.plot(x, f(x), color="#C0504D", label="$f(x)$")
for i in range(0, n, 2):
    x0, xm, x1 = a + i*h, a + (i+1)*h, a + (i+2)*h
    coeff = np.polyfit([x0, xm, x1], [f(x0), f(xm), f(x1)], 2)
    xx = np.linspace(x0, x1, 80)
    ax.plot(xx, np.polyval(coeff, xx), color="#4472C4", label="quadratic interpolation" if i == 0 else None)
    ax.plot([x0, xm, x1], [f(x0), f(xm), f(x1)], "o", color="#4472C4", markersize=3)
ax.set(xlim=(a, b), xlabel="$x$", ylabel="$f(x)$", title="Composite Simpson rule ($N=4$)")
ax.legend(frameon=False)
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(out / "simpson_rule.pdf")
plt.close(fig)

exact = 6.4
ns = 2**np.arange(1, 8)
mid_errors, trap_errors, simpson_errors = [], [], []
for count in ns:
    step = (b-a)/count
    mids = a + (np.arange(count)+.5)*step
    nodes = np.linspace(a,b,count+1)
    mid_value = step*np.sum(f(mids))
    trap_value = step*(.5*f(a) + np.sum(f(nodes[1:-1])) + .5*f(b))
    weights = np.ones(count+1); weights[1:-1:2] = 4; weights[2:-1:2] = 2
    simpson_value = step/3*np.sum(weights*f(nodes))
    mid_errors.append(abs(mid_value-exact))
    trap_errors.append(abs(trap_value-exact))
    simpson_errors.append(abs(simpson_value-exact))
fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.loglog(ns, mid_errors, "o-", label="midpoint: $O(N^{-2})$")
ax.loglog(ns, trap_errors, "s-", label="trapezoid: $O(N^{-2})$")
ax.loglog(ns, simpson_errors, "^-", label="Simpson: $O(N^{-4})$")
ax.set(xlabel="number of subintervals $N$", ylabel="absolute error", title="$\\int_0^2 (x^4-2x+2)\\,dx=6.4$")
ax.grid(True, which="both", alpha=.2)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(out / "quadrature_convergence.pdf")
plt.close(fig)

runge = lambda x: 1 / (1 + 25*x**2)
nodes = np.linspace(-1, 1, 17)
coeff = np.polynomial.polynomial.polyfit(nodes, runge(nodes), deg=16)
xx = np.linspace(-1, 1, 600)
fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.plot(xx, runge(xx), color="#C0504D", label="Runge function")
ax.plot(xx, np.polynomial.polynomial.polyval(xx, coeff), color="#4472C4", label="degree-16 interpolation")
ax.plot(nodes, runge(nodes), "o", color="#70AD47", markersize=3, label="equally spaced nodes")
ax.set(xlabel="$x$", ylabel="$f(x)$", title="Oscillation near the interval ends")
ax.set_ylim(-.5, 1.15)
ax.grid(alpha=.2)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(out / "runge_interpolation.pdf")
plt.close(fig)
