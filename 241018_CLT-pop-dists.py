import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the seaborn style for plots
sns.set(style="whitegrid")

# Create data for different distributions
x_normal = np.random.normal(loc=0, scale=1, size=1000)
x_bimodal = np.concatenate([np.random.normal(-2, 0.5, 500), np.random.normal(3, 1, 500)])
x_exponential = np.random.exponential(scale=1, size=1000)
x_poisson = np.random.poisson(lam=3, size=1000)
x_beta = np.random.beta(a=2, b=5, size=1000)
x_uniform = np.random.uniform(low=0, high=1, size=1000)

# Create new subplots for Probability Density Function (PDF) and Probability Mass Function (PMF) plots
fig, axes = plt.subplots(3, 2, figsize=(12, 12))

# Plot Normal Distribution PDF
sns.histplot(x_normal, bins=50, kde=True, ax=axes[0, 0], color="blue", stat="density")
axes[0, 0].set_title("Normal Distribution (PDF)")

# Plot Bimodal Distribution PDF
sns.histplot(x_bimodal, bins=50, kde=True, ax=axes[0, 1], color="green", stat="density")
axes[0, 1].set_title("Bimodal Distribution (PDF)")

# Plot Exponential Distribution PDF
sns.histplot(x_exponential, bins=50, kde=True, ax=axes[1, 0], color="red", stat="density")
axes[1, 0].set_title("Exponential Distribution (PDF)")

# Plot Poisson Distribution PMF
sns.histplot(x_poisson, bins=range(0, 15), discrete=True, kde=False, ax=axes[1, 1], color="purple", stat="density")
axes[1, 1].set_title("Poisson Distribution (PMF)")

# Plot Beta Distribution PDF
sns.histplot(x_beta, bins=50, kde=True, ax=axes[2, 0], color="orange", stat="density")
axes[2, 0].set_title("Beta Distribution (PDF)")

# Plot Uniform Distribution PDF
sns.histplot(x_uniform, bins=50, kde=True, ax=axes[2, 1], color="brown", stat="density")
axes[2, 1].set_title("Uniform Distribution (PDF)")

# Adjust layout
plt.tight_layout()

# save plot
plt.savefig('plots/241018_CLT-pop-dists.png')

# Show the updated plot
plt.show()
