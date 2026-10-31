from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out = Path(__file__).parent / "figures"
out.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 11, "axes.labelsize": 11, "axes.titlesize": 12})

x0 = 0.3 * np.pi
exact = np.cos(x0)
h = 10.0 ** (-np.arange(1, 17, dtype=float))
forward = (np.sin(x0 + h) - np.sin(x0)) / h
central = (np.sin(x0 + h) - np.sin(x0 - h)) / (2 * h)

fig, ax = plt.subplots(figsize=(6.6, 3.7))
ax.loglog(h, np.abs(forward - exact), "o-", color="#4472C4", label="forward difference")
ax.loglog(h, np.abs(central - exact), "s-", color="#ED7D31", label="central difference")
ax.set_xlabel("step size $h$")
ax.set_ylabel("absolute error")
ax.set_title("Derivative of sin(x) at x = 0.3 pi")
ax.invert_xaxis()
ax.grid(True, which="both", alpha=0.25)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(out / "differentiation_error.pdf")
plt.close(fig)
