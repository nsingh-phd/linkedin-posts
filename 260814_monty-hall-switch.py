"""Monty Hall: why switching doors wins two times out of three.

Top row  - all three equally likely worlds, played out. You always open on
           door 1; the host, who knows where the car is, must open a goat.
           Switching wins in two of the three worlds.
Bottom   - 10,000 simulated games for a player who always stays and one who
           always switches, converging on 1/3 and 2/3.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import Rectangle

# Shared palette (checked for colour-vision-deficiency separation)
BRASS = '#B4791E'  # switching
BLUE = '#2F5FA8'  # staying
PLUM = '#74203C'  # closed doors
INK = '#23131A'
MUTED = '#93808A'
GROUND = '#F5F0F1'


def simulate(n, switch, rng):
    """Play n games. Returns a boolean array of wins.

    The host knows where the car is and always opens a goat door, so
    switching wins exactly when the first pick was wrong.
    """
    car = rng.integers(0, 3, n)
    pick = rng.integers(0, 3, n)
    return pick != car if switch else pick == car


def draw_world(ax, car, pick=0):
    """Draw one world: three doors, the host's reveal, and the outcome."""
    # The host opens a goat door that is neither your pick nor the car.
    opened = next(d for d in range(3) if d not in (pick, car))
    switched_to = next(d for d in range(3) if d not in (pick, opened))

    for d in range(3):
        x = d * 1.2
        if d == opened:  # swung open, revealing a goat
            ax.add_patch(Rectangle((x, 0), 1, 1.6, facecolor=GROUND,
                                   edgecolor=MUTED, lw=1.2, ls='--'))
            ax.text(x + .5, .8, 'GOAT', ha='center', va='center',
                    fontsize=8.5, color=MUTED, fontweight='bold')
        else:
            is_car = d == car
            ax.add_patch(Rectangle((x, 0), 1, 1.6, facecolor=PLUM,
                                   edgecolor=BRASS if is_car else PLUM, lw=2.2))
            ax.text(x + .5, .8, 'CAR' if is_car else str(d + 1), ha='center',
                    va='center', fontsize=10 if is_car else 15,
                    color=BRASS if is_car else '#FCF4F6', fontweight='bold')

        # pick, opened and switched_to are always three different doors
        label = {pick: 'your pick', opened: 'host opens',
                 switched_to: 'still shut'}[d]
        ax.text(x + .5, -.22, label, ha='center', va='top', fontsize=7.5,
                color=INK if d == pick else MUTED)

    # Outcome strip beneath the doors
    switch_wins = switched_to == car
    ax.text(1.8, -.72, 'stay', ha='right', va='center', fontsize=8.5, color=MUTED)
    ax.text(1.9, -.72, 'lose' if switch_wins else 'WIN', ha='left', va='center',
            fontsize=8.5, fontweight='bold', color=MUTED if switch_wins else BLUE)
    ax.text(1.8, -1.02, 'switch', ha='right', va='center', fontsize=8.5, color=MUTED)
    ax.text(1.9, -1.02, 'WIN' if switch_wins else 'lose', ha='left', va='center',
            fontsize=8.5, fontweight='bold', color=BRASS if switch_wins else MUTED)

    ax.set_title(f'Car behind door {car + 1}', fontsize=10, color=INK, pad=10)
    ax.set_xlim(-.35, 3.55)
    ax.set_ylim(-1.35, 1.85)
    ax.set_aspect('equal')
    ax.axis('off')


def make_figure(n_games=10_000, seed=12345):
    rng = np.random.default_rng(seed)

    fig = plt.figure(figsize=(11, 8.5), facecolor=GROUND)
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1.7], hspace=.05, wspace=.15)

    # --- top: the three worlds -------------------------------------------
    for car in range(3):
        ax = fig.add_subplot(gs[0, car])
        ax.set_facecolor(GROUND)
        draw_world(ax, car=car)

    # --- bottom: 10,000 games --------------------------------------------
    ax = fig.add_subplot(gs[1, :])
    ax.set_facecolor(GROUND)

    games = np.arange(1, n_games + 1)
    final = {}
    for switch, colour, label in ((False, BLUE, 'Always stay'),
                                  (True, BRASS, 'Always switch')):
        rate = np.cumsum(simulate(n_games, switch, rng)) / games
        final[label] = rate[-1]
        ax.plot(games, rate, color=colour, lw=1.8, solid_joinstyle='round')
        ax.annotate(f'{label}\n{rate[-1]:.1%}', xy=(n_games, rate[-1]),
                    xytext=(12, 0), textcoords='offset points', va='center',
                    fontsize=10, fontweight='bold', color=colour)

    for y, txt in ((1 / 3, '1/3'), (2 / 3, '2/3')):
        ax.axhline(y, color=MUTED, ls='--', lw=1, zorder=0)
        # x in axes fraction, y in data units - the x axis is logarithmic
        ax.text(-.015, y, txt, transform=ax.get_yaxis_transform(),
                ha='right', va='center', fontsize=9, color=MUTED,
                fontweight='bold')

    ax.set_xlim(1, n_games)
    ax.set_ylim(0, 1)
    ax.set_xscale('log')
    ax.set_xlabel('Games played (log scale)', fontsize=10, color=INK)
    ax.set_ylabel('Share of games won', fontsize=10, color=INK)
    ax.set_yticks([0, .25, .5, .75, 1])
    ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
    ax.tick_params(colors=MUTED, labelsize=9)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(MUTED)
    ax.grid(True, axis='y', alpha=.15, color=MUTED)

    ax.text(.99, .04, 'https://n.singh.phd', transform=ax.transAxes,
            fontsize=9, ha='right', va='bottom', color=MUTED)

    fig.suptitle('Monty Hall: switching wins two times in three', fontsize=17,
                 fontweight='bold', color=INK, y=.97)
    fig.text(.5, .925, 'Your first pick is right 1 time in 3 - so switching, '
             'which flips that verdict, is right the other 2',
             ha='center', fontsize=11, color=MUTED)

    fig.savefig('plots/260814_monty-hall-switch.png', dpi=150,
                facecolor=GROUND, bbox_inches='tight')

    print(f'{n_games:,} games -> '
          + ', '.join(f'{k.lower()} {v:.1%}' for k, v in final.items()))


if __name__ == '__main__':
    make_figure()
