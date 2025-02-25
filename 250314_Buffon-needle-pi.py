import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

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
    
    if visualize and n <= 1000 and ax is not None:
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
        ax.set_title(f"n={n}, π={pi_est:.4f}, Err={abs(np.pi - pi_est):.4f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(0, d)
        ax.set_ylim(-0.5, 2.5*d)
        ax.grid(True, alpha=0.3)
    
    return pi_est

def plot_pi_convergence(max_n, step=100, l=1, d=2, ax=None):
    """
    Plot convergence of estimated pi to true pi.

    Parameters:
    max_n: int - maximum number of needles
    step: int - increment of n between simulations
    l: float - length of needle
    d: float - distance between lines
    ax: matplotlib.axes - axis to plot on (optional)

    Returns:
    tuple - (n_values, pi_estimates)
    """
    n_values = range(step, max_n + 1, step)
    pi_estimates = [buffon_needle_simulation(n, l, d, visualize=False) for n in n_values]
    
    if ax is not None:
        ax.plot(n_values, pi_estimates, 'b-', label='Estimated π')
        ax.axhline(y=np.pi, color='r', linestyle='--', label='True π')
        ax.set_xlabel('Number of Needles (n)')
        ax.set_ylabel('Estimated π')
        ax.set_title('Convergence of Estimated π')
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    return n_values, pi_estimates

def run_tests(l=1, d=2):
    """
    Run simulations and display results in a custom grid layout.

    Parameters:
    l: float - length of needle
    d: float - distance between lines
    """
    # Set up figure and GridSpec layout
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])  # 2 rows, 2 columns
    
    # First row: Two needle simulations
    test_ns = [100, 1000]
    axs = [plt.subplot(gs[0, 0]), plt.subplot(gs[0, 1])]  # Two columns in first row
    
    for idx, n in enumerate(test_ns):
        pi_estimate = buffon_needle_simulation(n, l, d, visualize=True, ax=axs[idx])
        print(f"Number of needles: {n}")
        print(f"Estimated π: {pi_estimate:.4f}")
        print(f"Absolute error: {abs(np.pi - pi_estimate):.4f}")
        print("-" * 40)
    
    # Second row: Convergence plot spanning both columns
    ax_conv = plt.subplot(gs[1, :])  # Span across both columns
    n_values, pi_estimates = plot_pi_convergence(max_n=10000, step=500, l=l, d=d, ax=ax_conv)
    print(f"Final estimate with n=10000: {pi_estimates[-1]:.4f}")
    print(f"Absolute error: {abs(np.pi - pi_estimates[-1]):.4f}")
    
    # Add overall title and adjust layout
    fig.suptitle(f"Buffon's Needle Experiment (l={l}, d={d})", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    np.random.seed(42)
    run_tests()