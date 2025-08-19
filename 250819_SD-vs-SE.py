"""
Standard Deviation vs Standard Error Visualization

This module demonstrates the relationship between standard deviation (SD) and 
standard error (SE) as sample size increases. It generates an animated plot 
showing how SD remains relatively constant while SE decreases as sample size grows.

Author: N. Singh, PhD
Date: August 19, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class SDvsSE:
    """
    A class to demonstrate the relationship between Standard Deviation (SD) and 
    Standard Error (SE) as sample size varies.
    """
    
    def __init__(self, n=10000, mean=0, sd=1, seed=12345):
        """
        Initialize the SDvsSE class with population parameters.
        
        Parameters:
        -----------
        n : int, optional (default=10000)
            Size of the population from which samples will be drawn
        mean : float, optional (default=0)
            Mean of the normal distribution
        sd : float, optional (default=1)
            Standard deviation of the normal distribution (population parameter)
        seed : int, optional (default=12345)
            Random seed for reproducibility
        """
        self.rng = np.random.default_rng(seed)
        self.data = self.rng.normal(loc=mean, scale=sd, size=n)
        self.n = n
        self.mean = mean
        self.sd = sd
        # Storage for samples and calculated statistics
        self.n_samples: dict = {}
        self.n_sample_sizes: list = []
        self.sds: list = []
        self.ses: list = []

    def get_random_sample(self, size):
        """
        Draw a random sample of specified size from the population.
        
        Parameters:
        -----------
        size : int
            Number of observations to sample
            
        Returns:
        --------
        numpy.ndarray
            Random sample of the specified size
        """
        return self.rng.choice(self.data, size=size)

    def generate_n_random_samples(self, sizes):
        """
        Generate multiple random samples with different sizes.
        
        Parameters:
        -----------
        sizes : array-like
            List or array of sample sizes to generate
            
        Notes:
        ------
        Results are stored in self.n_samples as a dictionary with
        sizes as keys and sample arrays as values
        """
        self.n_samples = {size: self.get_random_sample(size) for size in sizes}

    def calc_stats(self):
        """
        Calculate standard deviation and standard error for all generated samples.
        
        For each sample:
        - Calculates sample standard deviation (using Bessel's correction, ddof=1)
        - Calculates standard error (SD / sqrt(n))
        - Stores results in class attributes for plotting
        
        Notes:
        ------
        Results are stored in self.sds, self.ses, and self.n_sample_sizes arrays
        """
        for size, sample in self.n_samples.items():
            sd = np.std(sample, ddof=1)  # Sample standard deviation
            se = sd / np.sqrt(size)      # Standard error
            self.sds.append(sd)
            self.ses.append(se)
            self.n_sample_sizes.append(size)
        # Convert lists to numpy arrays for easier plotting
        self.sds = np.array(self.sds)
        self.ses = np.array(self.ses)
        self.n_sample_sizes = np.array(self.n_sample_sizes)

    def plot_sd_vs_se(self, output_path):
        """
        Create an animated plot showing SD vs SE as sample size increases.
        
        Parameters:
        -----------
        output_path : str
            Path where the animated GIF will be saved
            
        Notes:
        ------
        - Blue line shows Standard Deviation (relatively constant)
        - Red line shows Standard Error (decreases with sample size)
        - Gray dashed line shows the true population standard deviation
        - Animation shows points appearing sequentially as sample size increases
        """
        fig, ax = plt.subplots()
        # Initialize empty lines for animation
        line_sd, = ax.plot([], [], 'b-o', label='SD', markersize=2)
        line_se, = ax.plot([], [], 'r-o', label='SE', markersize=2)
        # Add reference line for true population standard deviation
        ax.axhline(y=self.sd, color='lightgray', linestyle='--', zorder=0)

        # Set plot limits and labels
        ax.set_xlim(self.n_sample_sizes.min(), self.n_sample_sizes.max())
        ax.set_ylim(0, self.sds.max() + 0.1)

        ax.set_xlabel("Sample Size")
        ax.set_ylabel("Standard Deviation and Standard Error")
        ax.set_title("Impact of increased sample size on \n standard deviation and standard error", fontsize=14)

        # Add watermark
        ax.text(x=9500, y=0.2, s="https://n.singh.phd", fontsize=10, color="gray", ha="right")
        ax.legend()

        def update(frame):
            """Animation function: updates lines with data up to current frame."""
            line_sd.set_data(self.n_sample_sizes[:frame+1], self.sds[:frame+1])
            line_se.set_data(self.n_sample_sizes[:frame+1], self.ses[:frame+1])
            return line_sd, line_se

        # Create and save animation
        anim = FuncAnimation(
            fig, update, frames=len(self.n_sample_sizes),
            blit=True, repeat=False
        )
        anim.save(output_path, writer='pillow', fps=30)


if __name__ == "__main__":
    # Main execution block: demonstrates the SD vs SE relationship.
    # Creates a population of 10,000 normally distributed values, then:
    # 1. Generates samples of varying sizes (50 to 10,000 in steps of 100)
    # 2. Calculates SD and SE for each sample size
    # 3. Creates an animated visualization showing the relationship
    
    sd_vs_se = SDvsSE(n=10000, mean=0, sd=1)
    sample_sizes = np.arange(50, 10000, 100)
    sd_vs_se.generate_n_random_samples(sample_sizes)
    sd_vs_se.calc_stats()
    sd_vs_se.plot_sd_vs_se(output_path='plots/250819_SD_vs_SE.gif')
