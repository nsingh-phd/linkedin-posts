"""
Does speeding really save time? A visualization for LinkedIn.

Shows estimated real-world minutes saved:
- Panel 1: Multiple trip distances at a 60 mph speed limit.
- Panel 2: Fixed 60-mile trip at three speed limits (35, 55, 75 mph).

Real-world time savings are shown as a plausible range (30-60% of idealized)
to account for traffic, signals, and non-highway segments where sustained
speeding is impractical (anchored to FHWA Travel Time Index context).

References:
- FHWA Travel Time Index: https://ops.fhwa.dot.gov/publications/fhwahop08054/sect6.htm

Author: N. Singh, PhD
Date: March 25, 2026
"""

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class SpeedingConfig:
    """Configuration for the speeding time-saved analysis."""

    baseline_mph: float
    trip_miles_list: list[float]
    mph_over_range: np.ndarray
    real_world_gain_factor_low: float
    real_world_gain_factor_high: float
    distance_colors: list[str]


class SpeedingAnalysis:
    """Compute idealized and real-world time savings from speeding."""

    def __init__(self, config: SpeedingConfig):
        self.config = config

    def time_saved_idealized(self, trip_miles: float) -> np.ndarray:
        """Minutes saved per trip from pure speed increase (no friction)."""
        cfg = self.config
        actual_mph = cfg.baseline_mph + cfg.mph_over_range
        return 60.0 * trip_miles * (1.0 / cfg.baseline_mph - 1.0 / actual_mph)

    def time_saved_real_world_low(self, trip_miles: float) -> np.ndarray:
        """Lower bound of real-world minutes saved (conservative dilution)."""
        return (
            self.time_saved_idealized(trip_miles)
            * self.config.real_world_gain_factor_low
        )

    def time_saved_real_world_high(self, trip_miles: float) -> np.ndarray:
        """Upper bound of real-world minutes saved (optimistic dilution)."""
        return (
            self.time_saved_idealized(trip_miles)
            * self.config.real_world_gain_factor_high
        )


def build_default_config(baseline_mph: float) -> SpeedingConfig:
    """Create default US-focused config for a given speed-limit baseline."""
    return SpeedingConfig(
        baseline_mph=baseline_mph,
        trip_miles_list=[10.0, 30.0, 70.0],
        mph_over_range=np.arange(1.0, 26.0, 1.0),
        real_world_gain_factor_low=0.30,
        real_world_gain_factor_high=0.60,
        distance_colors=['tab:blue', 'tab:orange', 'tab:green'],
    )


if __name__ == '__main__':
    # Panel 1: 60 mph limit, multiple distances
    ana_distances = SpeedingAnalysis(build_default_config(baseline_mph=60.0))

    # Panel 2: 60-mile trip, multiple speed limits
    speed_baselines = [35.0, 55.0, 75.0]
    speed_colors = ['tab:blue', 'tab:orange', 'tab:green']
    speed_analyses = []
    speed_labels = []
    for i, base in enumerate(speed_baselines):
        cfg = SpeedingConfig(
            baseline_mph=base,
            trip_miles_list=[60.0],
            mph_over_range=np.arange(1.0, 26.0, 1.0),
            real_world_gain_factor_low=0.30,
            real_world_gain_factor_high=0.60,
            distance_colors=[speed_colors[i]],
        )
        speed_analyses.append(SpeedingAnalysis(cfg))
        speed_labels.append(f'{int(base)} mph')

    # Custom 2-panel figure
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    # --- Panel 1: multiple distances, single baseline ---
    cfg1 = ana_distances.config
    x = cfg1.mph_over_range

    y_max = 0.0
    for miles in cfg1.trip_miles_list:
        y_max = max(y_max, ana_distances.time_saved_real_world_high(miles).max())
    for sa in speed_analyses:
        y_max = max(
            y_max, sa.time_saved_real_world_high(sa.config.trip_miles_list[0]).max()
        )
    y_max *= 1.15

    ax1 = axes[0]
    ax1.set_xlim(x.min(), x.max())
    ax1.set_ylim(0, y_max)
    ax1.set_xlabel('MPH over the speed limit')
    ax1.set_ylabel('Minutes saved')
    ax1.set_title('60 mph limit, by trip distance', fontsize=12, fontweight='bold')
    ax1.grid(alpha=0.25)

    for i, miles in enumerate(cfg1.trip_miles_list):
        color = cfg1.distance_colors[i]
        label = f'{int(miles)} mi'
        lo = ana_distances.time_saved_real_world_low(miles)
        hi = ana_distances.time_saved_real_world_high(miles)
        ax1.fill_between(x, lo, hi, color=color, alpha=0.25)
        ax1.plot(x, lo, color=color, lw=1, alpha=0.6)
        ax1.plot(x, hi, color=color, lw=1, alpha=0.6, label=label)
    ax1.legend(loc='upper left', fontsize=9)

    # --- Panel 2: fixed 60 mi, multiple baselines ---
    ax2 = axes[1]
    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim(0, y_max)
    ax2.set_xlabel('MPH over the speed limit')
    ax2.set_title('60-mile trip, by speed limit', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.25)

    colors2 = ['tab:blue', 'tab:orange', 'tab:green']
    for i, sa in enumerate(speed_analyses):
        miles = sa.config.trip_miles_list[0]
        color = colors2[i]
        label = speed_labels[i]
        lo = sa.time_saved_real_world_low(miles)
        hi = sa.time_saved_real_world_high(miles)
        ax2.fill_between(x, lo, hi, color=color, alpha=0.25)
        ax2.plot(x, lo, color=color, lw=1, alpha=0.6)
        ax2.plot(x, hi, color=color, lw=1, alpha=0.6, label=label)
    ax2.legend(loc='upper left', fontsize=9)

    fig.suptitle(
        'Does Speeding Really Save Time?',
        fontsize=14,
        fontweight='bold',
    )
    fig.text(
        0.5,
        0.01,
        'Real-world range assumes 30\u201360% of idealized savings are '
        'achievable (traffic, signals, non-highway segments; FHWA TTI context).',
        ha='center',
        fontsize=8,
        color='dimgray',
    )
    fig.text(
        0.99,
        0.01,
        'https://n.singh.phd',
        ha='right',
        fontsize=9,
        color='gray',
    )

    fig.tight_layout(rect=(0.0, 0.03, 1.0, 0.95))
    fig.savefig('plots/260325_speeding-time-saved.png', dpi=200)
    plt.close(fig)
    print('Saved combined plot.')
