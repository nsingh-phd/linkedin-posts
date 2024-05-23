# import modules
import numpy as np
import matplotlib.pyplot as plt

# set seed for reproducibility
np.random.seed(0)

# parameters for the normal distribution
vals = [1,2,3,4,5,6]
population_mean = np.mean(vals)
population_std = np.std(vals)

# different sample sizes
sample_sizes = [10, 100, 1000, 10000]

# create a figure with 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

for i, sample_size in enumerate(sample_sizes):
    # Generate random samples
    samples = np.random.normal(loc=population_mean, scale=population_std, size=sample_size)

    # Compute the cumulative average of the samples
    cumulative_avg = np.cumsum(samples) / np.arange(1, sample_size + 1)

    # Select the subplot
    ax = axs[i//2, i%2]

    # Plot the cumulative average
    ax.plot(cumulative_avg, label=f'Sample Size = {sample_size}')
    ax.axhline(y=population_mean, color='r', linestyle='--', label='Population Mean')
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Sample Average')
    ax.set_title(f'Sample Size = {sample_size}')
    ax.legend()
    ax.grid(True)

# adjust layout for better spacing
plt.tight_layout()
plt.show()
