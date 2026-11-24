from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out = Path(__file__).parent / "figures"
out.mkdir(exist_ok=True)
# Figure size matches the printed width in slide.tex, so the font sizes below
# are the sizes seen on the slide.
plt.rcParams.update({
    "font.family": ["Noto Sans CJK JP", "IPAexGothic", "sans-serif"],
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
})

x0 = 0.3 * np.pi
exact = np.cos(x0)
h = 10.0 ** (-np.arange(1, 17, dtype=float))
forward = (np.sin(x0 + h) - np.sin(x0)) / h
central = (np.sin(x0 + h) - np.sin(x0 - h)) / (2 * h)
err_forward = np.abs(forward - exact)
err_central = np.abs(central - exact)

fig, ax = plt.subplots(figsize=(3.5, 2.0))
ax.loglog(h, err_forward, "o-", ms=2.6, lw=1.1, color="#4472C4",
          label="forward difference")
ax.loglog(h, err_central, "s-", ms=2.6, lw=1.1, color="#ED7D31",
          label="central difference")
ax.set_xlabel("step size $h$")
ax.set_ylabel("absolute error")
ax.set_title("Derivative of sin(x) at x = 0.3 pi")
ax.invert_xaxis()
ax.set_ylim(1e-14, 3.0)
ax.grid(True, which="both", alpha=0.25)
ax.legend(loc="lower center", ncol=2, frameon=False, fontsize=7,
          handlelength=1.5, borderaxespad=0.15, columnspacing=1.2,
          handletextpad=0.4)

ax.text(1e-6, 1.4, "大きい $h$\n打ち切り誤差が支配",
        ha="center", va="top", fontsize=8)
ax.text(1e-13, 1.2e-9, "小さい $h$\n丸め誤差が支配",
        ha="center", va="center", fontsize=8)

fig.tight_layout(pad=0.25)
fig.savefig(out / "differentiation_error.pdf")
plt.close(fig)
