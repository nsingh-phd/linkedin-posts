"""
LinkedIn carousel generator for the speeding-time-saved analysis.

Produces a multi-slide PDF (1080x1350 px per slide, 4:5 aspect) suitable for uploading
as a LinkedIn carousel document post.

Author: N. Singh, PhD
Date: March 26, 2026
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# ── Design tokens ──────────────────────────────────────────────────────
BG = '#F5C518'  # gold
TEXT = '#1A1A1A'  # near-black
ACCENT = '#8B4513'  # saddle brown
SUBTLE = '#5C3A1E'  # dark brown
DIM = '#9E7C4F'  # muted tan
HIGHLIGHT = '#C62828'  # deep red
SLIDE_SIZE = (10.8, 13.5)  # 4:5 aspect at 100 dpi → 1080x1350
DPI = 100
FONT_TITLE = 42
FONT_BODY = 26
FONT_BIG = 56
FONT_SMALL = 20
FONT_WATERMARK = 16
WATERMARK = 'n.singh.phd'
PAD = 0.08  # fractional margin


def _base_slide(fig_kw=None):
    """Create a blank slide with the standard background."""
    fig = plt.figure(figsize=SLIDE_SIZE, dpi=DPI, **(fig_kw or {}))
    fig.set_facecolor(BG)
    fig.text(
        0.5,
        0.02,
        WATERMARK,
        ha='center',
        fontsize=FONT_WATERMARK,
        color=DIM,
        style='italic',
    )
    return fig


def _wrap(text, max_chars=45):
    """Naive word-wrap into lines of ≤ max_chars."""
    words = text.split()
    lines, line = [], ''
    for w in words:
        if line and len(line) + len(w) + 1 > max_chars:
            lines.append(line)
            line = w
        else:
            line = f'{line} {w}'.strip()
    if line:
        lines.append(line)
    return '\n'.join(lines)


# ── Slide builders ─────────────────────────────────────────────────────


def slide_cover():
    """Slide 1: bold hook title."""
    fig = _base_slide()
    fig.text(
        0.5,
        0.58,
        'Does Speeding\nActually Save\nYou Time?',
        ha='center',
        va='center',
        fontsize=FONT_BIG,
        fontweight='bold',
        color=TEXT,
        linespacing=1.4,
    )
    fig.text(
        0.5,
        0.34,
        'Not really. Here\u2019s why.',
        ha='center',
        va='center',
        fontsize=FONT_TITLE,
        color=ACCENT,
    )
    fig.text(
        0.5,
        0.24,
        'Swipe \u2192',
        ha='center',
        va='center',
        fontsize=FONT_BODY,
        color=DIM,
    )
    return fig


def slide_setup():
    """Slide 2: relatable hook + what I did."""
    fig = _base_slide()
    fig.text(
        0.5,
        0.82,
        'We\u2019ve all been there',
        ha='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=ACCENT,
    )
    body = (
        'You\u2019re running late, so you speed up\n'
        'thinking you\u2019ll make up time.\n\n'
        'But later you wonder\u2026\n'
        '\u201cWas it really worth it?\u201d\n\n'
        'I ran a simulation to find out\n'
        'how many minutes you actually save\n'
        'by going over the speed limit.'
    )
    fig.text(
        0.5,
        0.48,
        body,
        ha='center',
        va='center',
        fontsize=FONT_BODY,
        color=TEXT,
        linespacing=1.6,
    )
    return fig


def slide_method():
    """Slide 3: what the analysis shows."""
    fig = _base_slide()
    fig.text(
        0.5,
        0.85,
        'The Approach',
        ha='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=ACCENT,
    )
    body = (
        'The math is simple:\n'
        'time = distance \u00f7 speed\n\n'
        'But real-world driving isn\u2019t ideal.\n'
        'Traffic, signals, and stop-and-go\n'
        'eat into your theoretical gains.\n\n'
        'Based on the FHWA Travel Time Index,\n'
        'only 30\u201360% of idealized savings\n'
        'are achievable in practice.'
    )
    fig.text(
        0.5,
        0.48,
        body,
        ha='center',
        va='center',
        fontsize=FONT_BODY,
        color=TEXT,
        linespacing=1.6,
    )
    return fig


def _build_analyses():
    """Build the analysis objects (reuse logic from the main script)."""
    # Panel 1: 60 mph, multiple distances
    from dataclasses import dataclass

    @dataclass
    class Cfg:
        baseline_mph: float
        trip_miles_list: list
        mph_over_range: np.ndarray
        real_world_gain_factor_low: float
        real_world_gain_factor_high: float
        distance_colors: list

    def _make(baseline, miles_list, colors):
        return Cfg(
            baseline_mph=baseline,
            trip_miles_list=miles_list,
            mph_over_range=np.arange(1.0, 26.0, 1.0),
            real_world_gain_factor_low=0.30,
            real_world_gain_factor_high=0.60,
            distance_colors=colors,
        )

    def _lo(cfg, m):
        actual = cfg.baseline_mph + cfg.mph_over_range
        ideal = 60.0 * m * (1.0 / cfg.baseline_mph - 1.0 / actual)
        return ideal * cfg.real_world_gain_factor_low

    def _hi(cfg, m):
        actual = cfg.baseline_mph + cfg.mph_over_range
        ideal = 60.0 * m * (1.0 / cfg.baseline_mph - 1.0 / actual)
        return ideal * cfg.real_world_gain_factor_high

    return Cfg, _make, _lo, _hi


def slide_chart_distances():
    """Slide 4: chart + key numbers — 60 mph limit, by trip distance."""
    Cfg, _make, _lo, _hi = _build_analyses()
    cfg = _make(60.0, [10.0, 30.0, 70.0], ['#8B4513', '#C62828', '#1A1A1A'])

    fig = _base_slide()
    ax = fig.add_axes([0.12, 0.32, 0.80, 0.46])
    ax.set_facecolor('#FFF8DC')  # cornsilk for chart area
    x = cfg.mph_over_range

    y_max = 0.0
    for m in cfg.trip_miles_list:
        y_max = max(y_max, _hi(cfg, m).max())
    y_max *= 1.15

    for i, m in enumerate(cfg.trip_miles_list):
        c = cfg.distance_colors[i]
        lo, hi = _lo(cfg, m), _hi(cfg, m)
        ax.fill_between(x, lo, hi, color=c, alpha=0.25)
        ax.plot(x, lo, color=c, lw=1.5, alpha=0.7)
        ax.plot(x, hi, color=c, lw=3, alpha=0.7, label=f'{int(m)} mi')

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, y_max)
    ax.set_xlabel('MPH over the speed limit', color=TEXT, fontsize=FONT_SMALL)
    ax.set_ylabel('Minutes saved', color=TEXT, fontsize=FONT_SMALL)
    ax.tick_params(colors=TEXT, labelsize=FONT_SMALL - 2)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.grid(alpha=0.20, color='#B0B0B0')
    ax.legend(fontsize=FONT_SMALL, facecolor='#FFF8DC', edgecolor=DIM, labelcolor=TEXT)

    fig.text(
        0.5,
        0.86,
        '60 mph limit, by trip distance',
        ha='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=ACCENT,
    )

    # Key numbers below the chart
    rows = [
        ('10-mile trip, +25 mph over', '1\u20132 min saved', SUBTLE),
        ('30-mile trip, +25 mph over', '3\u20135 min saved', HIGHLIGHT),
        ('70-mile trip, +25 mph over', '5\u201310 min saved', '#1A1A1A'),
    ]
    y = 0.24
    for label, value, color in rows:
        fig.text(0.10, y, label, fontsize=FONT_SMALL, color=TEXT, va='center')
        fig.text(
            0.90,
            y,
            value,
            fontsize=FONT_SMALL,
            fontweight='bold',
            color=color,
            ha='right',
            va='center',
        )
        y -= 0.06

    return fig


def slide_chart_speeds():
    """Slide 6: chart — 60-mile trip, by speed limit."""
    Cfg, _make, _lo, _hi = _build_analyses()
    baselines = [35.0, 55.0, 75.0]
    colors = ['#8B4513', '#C62828', '#1A1A1A']

    fig = _base_slide()
    ax = fig.add_axes([0.12, 0.10, 0.80, 0.62])
    ax.set_facecolor('#FFF8DC')
    x = np.arange(1.0, 26.0, 1.0)

    y_max = 0.0
    for b in baselines:
        cfg = _make(b, [60.0], ['w'])
        y_max = max(y_max, _hi(cfg, 60.0).max())
    y_max *= 1.15

    for i, b in enumerate(baselines):
        cfg = _make(b, [60.0], [colors[i]])
        c = colors[i]
        lo, hi = _lo(cfg, 60.0), _hi(cfg, 60.0)
        ax.fill_between(x, lo, hi, color=c, alpha=0.25)
        ax.plot(x, lo, color=c, lw=1.5, alpha=0.7)
        ax.plot(x, hi, color=c, lw=3, alpha=0.7, label=f'{int(b)} mph limit')

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, y_max)
    ax.set_xlabel('MPH over the speed limit', color=TEXT, fontsize=FONT_SMALL)
    ax.set_ylabel('Minutes saved', color=TEXT, fontsize=FONT_SMALL)
    ax.tick_params(colors=TEXT, labelsize=FONT_SMALL - 2)
    for spine in ax.spines.values():
        spine.set_color(DIM)
    ax.grid(alpha=0.20, color='#B0B0B0')
    ax.legend(fontsize=FONT_SMALL, facecolor='#FFF8DC', edgecolor=DIM, labelcolor=TEXT)

    fig.text(
        0.5,
        0.82,
        '60-mile trip, by speed limit',
        ha='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=ACCENT,
    )
    return fig


def slide_physics():
    """Slide 7: the diminishing-returns insight."""
    fig = _base_slide()
    fig.text(
        0.5,
        0.85,
        'Why more gain at\nlower speed limits?\nDiminishing Returns.',
        ha='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=ACCENT,
    )
    body = (
        'At lower speed limits (35 mph),\n'
        'going +25 over saves 13\u201326 min.\n\n'
        'At higher speed limits (75 mph),\n'
        'the same +25 saves only 4\u20137 min.\n\n'
        'Each additional mph matters less\n'
        'as you go faster. It\u2019s baked\n'
        'right into the physics.\n\n'
        'Higher speed limit =\n'
        'less gain, bigger risk.'
    )
    fig.text(
        0.5,
        0.46,
        body,
        ha='center',
        va='center',
        fontsize=FONT_BODY,
        color=TEXT,
        linespacing=1.6,
    )
    return fig


def slide_takeaway():
    """Slide 8: closing CTA."""
    fig = _base_slide()
    fig.text(
        0.5,
        0.68,
        'Next time you\u2019re\ntempted to floor it\u2026',
        ha='center',
        va='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=TEXT,
        linespacing=1.4,
    )
    fig.text(
        0.5,
        0.46,
        'Remember: that extra speed\nis buying you a couple of minutes\nat best\u2014and costing you\na lot more in risk.',
        ha='center',
        va='center',
        fontsize=FONT_BODY,
        color=ACCENT,
        linespacing=1.5,
    )
    fig.text(
        0.5,
        0.22,
        'Happy learning!',
        ha='center',
        fontsize=FONT_TITLE,
        fontweight='bold',
        color=HIGHLIGHT,
    )
    fig.text(
        0.5,
        0.14,
        '#statbits  #statistics  #datascience',
        ha='center',
        fontsize=FONT_SMALL,
        color=DIM,
    )
    return fig


# ── Main ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    slides = [
        slide_cover(),
        slide_setup(),
        slide_method(),
        slide_chart_distances(),
        slide_chart_speeds(),
        slide_physics(),
        slide_takeaway(),
    ]

    out = 'plots/260325_speeding-carousel.pdf'
    with PdfPages(out) as pdf:
        for fig in slides:
            pdf.savefig(fig, facecolor=fig.get_facecolor(), dpi=DPI)
            plt.close(fig)

    print(f'Saved {len(slides)}-slide carousel to {out}')
