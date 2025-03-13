import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation

def buffon_needle_simulation(n, l=1, d=2, visualize=True, ax=None):
    """
    Simulate Buffon's Needle problem and estimate pi.

    Parameters:
    n: int - number of needles to drop
    l: float - length of needle (default=1)
    d: float - distance between lines (default=2)
    visualize: bool - whether to show needle visualization
    ax: matplotlib.axes - axis to plot on (optional)

    Returns:
    float - estimated value of pi
    """
    x = np.random.uniform(0, d/2, n)
    theta = np.random.uniform(0, np.pi/2, n)
    crossings = np.sum(x <= (l/2) * np.sin(theta))
    pi_est = float('inf') if crossings == 0 else (2 * l * n) / (d * crossings)
    
    if visualize and ax is not None:
        for i in range(-1, 3):
            ax.axhline(y=i*d, color='gray', linestyle='-', alpha=0.3)
        for i in range(n):
            x_center = x[i] + d/2
            y_center = np.random.uniform(0, 2*d)
            dx = (l/2) * np.cos(theta[i])
            dy = (l/2) * np.sin(theta[i])
            color = 'red' if x[i] <= (l/2) * np.sin(theta[i]) else 'blue'
            ax.plot([x_center - dx, x_center + dx], 
                    [y_center - dy, y_center + dy], 
                    color=color, alpha=0.5)
        ax.set_title(f"n={n}, π estimate={pi_est:.4f}, Error={abs(np.pi - pi_est):.4f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(0, d)
        ax.set_ylim(-0.5, 2.5*d)
        ax.grid(True, alpha=0.3, axis='y')
    
    return pi_est

def run_tests(l=1, d=2, max_n=25000, step=100):
    """
    Run simulations and display results with an animated convergence plot in a grid,
    saving the entire figure as a GIF.

    Parameters:
    l: float - length of needle
    d: float - distance between lines
    max_n: int - maximum number of needles for convergence
    step: int - increment of n between simulations
    """
    # Set up figure and GridSpec layout
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
    
    # First row: Two needle simulations (static)
    test_ns = [100, 1000]
    axs = [plt.subplot(gs[0, 0]), plt.subplot(gs[0, 1])]
    
    for idx, n in enumerate(test_ns):
        pi_estimate = buffon_needle_simulation(n, l, d, visualize=True, ax=axs[idx])
        print(f"Number of needles: {n}")
        print(f"Estimated π: {pi_estimate:.4f}")
        print(f"Absolute error: {abs(np.pi - pi_estimate):.4f}")
        print("-" * 40)
    
    # Second row: Animated convergence plot spanning both columns
    ax_conv = plt.subplot(gs[1, :])
    ax_conv.set_xlabel('Number of Needles (n)')
    ax_conv.set_ylabel('Estimated π')
    ax_conv.set_title('Convergence of Estimated π')
    ax_conv.grid(True, alpha=0.2)
    ax_conv.set_ylim(2.5, 4.0)
    ax_conv.set_xlim(step, max_n)
    ax_conv.axhline(y=np.pi, color='r', linestyle='--', label='True π')
    ax_conv.legend()

    # Data for animation
    n_values = list(range(step, max_n + 1, step))
    pi_estimates = [buffon_needle_simulation(n, l, d, visualize=False) for n in n_values]
    
    # Initialize line for animation
    line, = ax_conv.plot([], [], 'b-o', label='Estimated π', alpha=0.5)
    
    # Animation initialization function
    def init():
        line.set_data([], [])
        return line,
    
    # Animation update function
    def update(frame):
        line.set_data(n_values[:frame+1], pi_estimates[:frame+1])
        return line,
    
    # Create animation
    anim = FuncAnimation(fig, update, init_func=init, frames=len(n_values), 
                        interval=1, blit=True, repeat=False)
    
    # Add overall title and adjust layout
    fig.suptitle(f"Buffon's Needle Experiment (l={l}, d={d})", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save as GIF using Pillow writer
    anim.save('plots/250314_Buffon-needle-pi.gif', writer='pillow', fps=30)
    
    # Print final estimate
    print(f"Final estimate with n={max_n}: {pi_estimates[-1]:.4f}")
    print(f"Absolute error: {abs(np.pi - pi_estimates[-1]):.4f}")

if __name__ == "__main__":
    np.random.seed(12345)
    run_tests()