from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out = Path(__file__).parent / "figures"
out.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.labelsize": 10, "axes.titlesize": 11})
rng = np.random.default_rng(2026)

# Use the same seed, sample sizes, and generation order as week8.ipynb.
N_max = 1_000_000
x = rng.uniform(0.0, np.pi, size=N_max)
samples = np.pi * np.sin(x)
cumulative = np.cumsum(samples)
N_values = np.array([100, 1_000, 10_000, 100_000, 1_000_000])
estimates = cumulative[N_values - 1] / N_values
exact = 2.0
variance = np.pi**2 / 2 - exact**2
standard_errors = np.sqrt(variance / N_values)
fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.errorbar(N_values, estimates, yerr=3*standard_errors, fmt="o", capsize=3, label="estimate with $\\pm3$ standard errors")
ax.axhline(exact, color="#C0504D", linestyle="--", label="exact value: 2")
ax.set_xscale("log")
ax.set(xlabel="number of samples $N$", ylabel="integral estimate", title="$\\int_0^\\pi \\sin x\\,dx$")
ax.grid(alpha=.2)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(out / "sin_monte_carlo.pdf")
plt.close(fig)

N_plot = 1_000
points = rng.random((N_plot, 2))
inside = np.sum(points**2, axis=1) <= 1.0
angle = np.linspace(0, np.pi/2, 300)
fig, ax = plt.subplots(figsize=(5.5, 4.4))
ax.plot(np.cos(angle), np.sin(angle), color="black", label="quarter circle")
ax.scatter(points[inside, 0], points[inside, 1], s=8, color="#C0504D", label="inside")
ax.scatter(points[~inside, 0], points[~inside, 1], s=8, color="#4472C4", label="outside")
ax.set(xlabel="$x$", ylabel="$y$", xlim=(0, 1), ylim=(0, 1))
ax.set_aspect("equal")
ax.legend(frameon=False, markerscale=1.5)
fig.tight_layout()
fig.savefig(out / "circle_points.pdf")
plt.close(fig)

N_pi = 500_000
points_pi = rng.random((N_pi, 2))
inside_pi = np.sum(points_pi**2, axis=1) <= 1.0
cum_hits = np.cumsum(inside_pi)
checkpoints = np.array([100, 1_000, 10_000, 100_000, 500_000])
pi_estimates = 4*cum_hits[checkpoints-1]/checkpoints
pi_se = 4*np.sqrt((np.pi/4)*(1-np.pi/4)/checkpoints)
fig, ax = plt.subplots(figsize=(6.7, 3.5))
ax.errorbar(checkpoints, pi_estimates, yerr=3*pi_se, fmt="o", capsize=3, label="estimate with $\\pm3$ standard errors")
ax.axhline(np.pi, color="#C0504D", linestyle="--", label="$\\pi$")
ax.set_xscale("log")
ax.set(xlabel="number of samples $N$", ylabel="estimate of $\\pi$", title="Monte Carlo estimate of circle area")
ax.grid(alpha=.2)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(out / "pi_convergence.pdf")
plt.close(fig)

def action(x):
    return 0.5*x**2

def metropolis(steps, x_initial, random_generator):
    x = float(x_initial)
    chain = np.empty(steps + 1)
    chain[0] = x
    for i in range(steps):
        proposal = x + random_generator.uniform(-1.0, 1.0)
        probability = min(1.0, np.exp(action(x)-action(proposal)))
        if random_generator.random() < probability:
            x = proposal
        chain[i+1] = x
    return chain

chain = metropolis(50_000, 0.0, rng)
grid = np.linspace(-5, 5, 500)
normal = np.exp(-0.5*grid**2)/np.sqrt(2*np.pi)
fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.2), sharey=True)
for ax, count, bins in zip(axes, [100, 1_000, 50_000], [10, 25, 60]):
    ax.hist(chain[1:count+1], bins=bins, density=True, alpha=.55, label="MCMC")
    ax.plot(grid, normal, color="#C0504D", label="standard normal")
    ax.set_title(f"$N={count:,}$")
    ax.set_xlabel("$x$")
axes[0].set_ylabel("probability density")
axes[-1].legend(frameon=False)
fig.tight_layout()
fig.savefig(out / "metropolis_gaussian.pdf")
plt.close(fig)
