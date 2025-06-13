import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm, norm, expon

# Create a figure and a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Lognormal Distribution
mean = 0
sigma = 0.25
x = np.linspace(0, 6, 10000)
pdf = lognorm.pdf(x, s=sigma, scale=np.exp(mean))
axs[0, 0].plot(x, pdf, label=f'lognormal(μ={mean}, σ={sigma})', color='purple')
axs[0, 0].fill_between(x, pdf, alpha=0.2, color='purple')
axs[0, 0].set_title('Lognormal Distribution with PDF > 1')
axs[0, 0].set_xlabel('x')
axs[0, 0].set_ylabel('Probability Density')
axs[0, 0].set_ylim(0, max(pdf) + 0.1)
axs[0, 0].legend()
axs[0, 0].grid(True, linestyle=':')

# Uniform Distribution
a = 0
b = 0.5
x = np.linspace(a, b, 1000)
pdf = np.ones_like(x) / (b - a)
axs[0, 1].plot(x, pdf, label=f'uniform({a}, {b})')
axs[0, 1].fill_between(x, pdf, alpha=0.2)
axs[0, 1].set_title('Uniform Distribution PDF with PDF > 1')
axs[0, 1].set_xlabel('x')
axs[0, 1].set_ylabel('Probability Density')
axs[0, 1].set_ylim(0, max(pdf) + 0.5)
axs[0, 1].legend()
axs[0, 1].grid(True, linestyle=':')

# Normal Distribution
x = np.linspace(-2, 2, 1000)
mean = 0
std_dev = 0.2
pdf = norm.pdf(x, mean, std_dev)
axs[1, 0].plot(x, pdf, label=f'normal(μ={mean}, σ={std_dev})', color='green')
axs[1, 0].fill_between(x, pdf, color='lightgreen', alpha=0.5)
axs[1, 0].set_title('Normal Distribution with PDF > 1')
axs[1, 0].set_xlabel('x')
axs[1, 0].set_ylabel('Probability Density')
axs[1, 0].set_ylim(0, max(pdf) + 0.1)
axs[1, 0].legend()
axs[1, 0].grid(True, linestyle=':')

# Exponential Distribution
scale = 0.5
x = np.linspace(0, 2, 1000)
pdf = expon.pdf(x, scale=scale)
axs[1, 1].plot(x, pdf, label=f'exponential(Scale = {scale})', color='red')
axs[1, 1].fill_between(x, pdf, color='salmon', alpha=0.5)
axs[1, 1].set_title('Exponential Distribution with PDF > 1')
axs[1, 1].set_xlabel('x')
axs[1, 1].set_ylabel('Probability Density')
axs[1, 0].set_ylim(0, max(pdf) + 0.1)
axs[1, 1].legend()
axs[1, 1].grid(True, linestyle=':')

# Adjust layout
plt.tight_layout()

plt.savefig('plots/240814_PDFs_>_1_plots.png')

# Show the plot
plt.show()