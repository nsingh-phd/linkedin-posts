import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set random seed for reproducibility
np.random.seed(12345)

# Parameters for two normal distributions with negligible difference
mu1 = 10    # Mean of first distribution
mu2 = 10.01  # Mean of second distribution
sigma = 1.0   # Same standard deviation for both

# Sample sizes to test (logarithmic scale from 100 to 1,000,000)
sample_sizes = np.logspace(2, 6, num=100, dtype=int)
p_values = []

# Generate data and calculate p-values for each sample size
for n in sample_sizes:
    sample1 = np.random.normal(mu1, sigma, n)
    sample2 = np.random.normal(mu2, sigma, n)
    t_stat, p_val = stats.ttest_ind(sample1, sample2)
    p_values.append(p_val)

# Create animation
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(min(sample_sizes), max(sample_sizes))
ax.set_ylim(1e-15, 2)
ax.set_xlabel('Sample Size (n)')
ax.set_ylabel('p-value')
ax.set_title(f'p-value vs Sample Size\n(Comparing N({mu1},1) vs N({mu2},1))')
ax.grid(True, which="both", ls="-", alpha=0.2)

# Add significance line at 0.05
ax.axhline(y=0.05, color='r', linestyle='--', label='p = 0.05')
ax.legend(loc='lower left')

# Add website text at bottom right
website_text = ax.text(0.98, 0.02, 'https://n.singh.phd', 
                      transform=ax.transAxes, 
                      ha='right', 
                      va='bottom',
                      fontsize=10,
                      color='gray')

# Initial empty plot
line, = ax.plot([], [], 'b-', label='p-value trend')
scatter = ax.scatter([], [], c='blue', alpha=0.5)

def init():
    line.set_data([], [])
    scatter.set_offsets(np.zeros((0, 2)))  # Initialize with empty 2D array
    return line, scatter

def animate(i):
    # Update line plot
    line.set_data(sample_sizes[:i+1], p_values[:i+1])
    # Update scatter plot with proper 2D array
    data = np.column_stack((sample_sizes[:i+1], p_values[:i+1]))
    scatter.set_offsets(data)
    return line, scatter

# Create animation
anim = FuncAnimation(fig, animate, init_func=init,
                    frames=len(sample_sizes), interval=100, blit=True)

# Save animation
anim.save('plots/250221_sampleSize_pvalue.gif', writer='pillow')

# Show plot
plt.show()