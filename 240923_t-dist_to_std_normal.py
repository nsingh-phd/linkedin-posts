import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import imageio.v2 as imageio

# Set up values for the x-axis (range of values for the distributions)
x = np.linspace(-4, 4, 1000)

# Standard normal distribution (fixed for all frames)
normal_dist = stats.norm.pdf(x)

# List to store frames for the GIF
frames = []

# Create the t-distributions for df ranging from 1 to 100 and save each frame
for df in range(1, 31):
    t_dist = stats.t.pdf(x, df)
    
    # Create the plot
    plt.figure(figsize=(6, 4))
    plt.plot(x, normal_dist, label="Standard Normal", color='gray', linestyle='--', linewidth=2)
    plt.plot(x, t_dist, label=f"t-distribution (df={df})", color='red', linewidth=2)
    plt.title(f"t-distribution Converging to Normal (df = {df})")
    plt.text(1.5, 0.35, "https://n.singh.phd", fontsize=10, color="gray")
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.ylim(0, 0.45)
    plt.legend()
    
    # Save the current plot as a frame
    plt.savefig('plots/240923_t-dist_to_std_normal.png')
    frames.append(imageio.imread('plots/240923_t-dist_to_std_normal.png'))
    plt.close()

# Save the frames as an animated GIF
gif_path = 'plots/240923_t-dist_to_std_normal.gif'
imageio.mimsave(gif_path, frames, fps=5, loop=0)


