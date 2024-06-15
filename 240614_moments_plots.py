import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, t, truncnorm, skew, kurtosis

# --- CONFIGURATION ---
NUM_SAMPLES = 10000
DISTRIBUTIONS = {
    "Normal": {"dist": norm, "params": {"loc": 0, "scale": 1}, "color": "skyblue"},
    "Right-Skewed (Exponential)": {"dist": expon, "params": {"scale": 1}, "color": "salmon"},
    "Leptokurtic (t-distribution)": {"dist": t, "params": {"df": 3}, "color": "lightgreen"},
    "Platykurtic (Truncated Normal)": {
        "dist": truncnorm,
        "params": {"a": -1.5, "b": 1.5, "loc": 0, "scale": 1},
        "color": "orange",
    },
}

# --- HELPER FUNCTIONS ---
def calculate_stats(samples):
    """Calculates mean, variance, skewness, and kurtosis of a sample."""
    return [np.round(func(samples), 3) for func in (np.mean, np.var)] + [
        round(skew(samples), 3),
        round(kurtosis(samples), 3),
    ]

def format_stats(stats):
    """Formats statistics into a string for plot legends."""
    return (
        f"Mean: {stats[0]}\nVar: {stats[1]}\nSkew: {stats[2]}\nKurt: {stats[3]}"
    )

# --- PLOTTING ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

for i, (title, config) in enumerate(DISTRIBUTIONS.items()):
    # Sample generation
    samples = config["dist"].rvs(size=NUM_SAMPLES, **config["params"])

    # Calculate and format statistics
    stats = calculate_stats(samples)
    stats_legend = format_stats(stats)

    # Plot
    ax = axs[i // 2, i % 2]  # Determine subplot position
    ax.hist(samples, bins=30, density=True, alpha=0.7, color=config["color"], label=stats_legend)
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")

    # Theoretical PDF
    x = np.linspace(min(samples), max(samples), 100)
    pdf = config["dist"].pdf(x, **config["params"])
    ax.plot(x, pdf, "r", linewidth=2)
    ax.legend(loc="upper right")

# --- WATERMARK ---
fig.text(
    0.985,
    0.7,
    "@nsinghphd",
    horizontalalignment="right",
    verticalalignment="top",
    fontsize=12,
    fontweight="bold",
    rotation=90,
)

plt.tight_layout()
plt.savefig('plots/240614_moments_plots.png')
plt.show()
