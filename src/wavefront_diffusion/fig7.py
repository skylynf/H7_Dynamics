#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate SVG outputs for multiple datasets (H7, H7N3, H7N7, H7N9)
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, LogLocator, LogFormatterMathtext

# ---------------------------------------------------------------------
# Global Aesthetic Parameters
# ---------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "axes.linewidth": 1.5,
    "axes.edgecolor": "black",
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "xtick.color": "black",
    "ytick.color": "black",
    "xtick.major.size": 4,
    "xtick.major.width": 1.2,
    "ytick.major.size": 4,
    "ytick.major.width": 1.2,
    "legend.fontsize": 9,
    "figure.dpi": 600
})

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------
def short_formatter(x, pos):
    """Formatter for axis ticks (k for thousand, M for million)."""
    if x == 0:
        return "0"
    abs_x = abs(x)
    if abs_x >= 1e6:
        v = x / 1e6
        return f"{v:.1f} M" if v % 1 else f"{int(v)} M"
    if abs_x >= 1e3:
        v = x / 1e3
        return f"{v:.1f} k" if v % 1 else f"{int(v)} k"
    return f"{int(x)}"

def tidy_spines(ax):
    """Only keep bottom and left spines."""
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

# ---------------------------------------------------------------------
# Input Files and Corresponding Output Names
# ---------------------------------------------------------------------
input_files = ["H7.xlsx", "H7N3.xlsx", "H7N7.xlsx", "H7N9.xlsx"]

sheets = {
    "wave_host":           "median_wavedistance",
    "wave_wild":           "wild_demostic_wavefront",
    "diff_host_weighted":  "diffusion_coefficient_weighted",
    "diff_wild_weighted":  "wild_domestic_weightcoefficient"
}

palette_host = {"ANSERIFORMES": "black", "GALLIFORMES": "red"}
fill_host = {"ANSERIFORMES": "#abddff", "GALLIFORMES": "#ffc2c2"}
palette_wild = {"wild": "purple", "domestic": "orange"}
fill_wild = {"wild": "#dab5ff", "domestic": "#ffd9b3"}

# ---------------------------------------------------------------------
# Generate Plots for Each Input File
# ---------------------------------------------------------------------
for input_file in input_files:
    excel_path = pathlib.Path(input_file)
    output_name = excel_path.stem  # Use the file name (without extension)

    # Read data from the Excel file
    df = {k: pd.read_excel(excel_path, sheet_name=v) for k, v in sheets.items()}

    # Configure the log-ticks for log-scaled plots
    log_major = LogLocator(base=10, subs=(1,), numticks=6)
    log_minor = LogLocator(base=10, subs=tuple(i / 10 for i in range(1, 10)), numticks=10)
    log_fmt = LogFormatterMathtext(base=10)

    # Create subplots
    fig, axes = plt.subplots(4, 1, figsize=(4, 12), sharex=False)

    # (1) Host-specific wavefront distance
    ax = axes[0]
    for grp, sub in df["wave_host"].groupby("group"):
        ax.plot(sub["time"], sub["distance"], lw=3, color=palette_host[grp], label=grp)
        ax.fill_between(sub["time"], sub["low"], sub["high"], color=fill_host[grp], alpha=0.7, linewidth=0)
    ax.set_xlim(2000, 2025)
    ax.set_ylim(0, 20000)
    ax.set_xticks(range(2000, 2026, 5))
    ax.set_yticks(range(0, 20001, 5000))
    ax.yaxis.set_major_formatter(FuncFormatter(short_formatter))
    ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.6, axis="y")
    tidy_spines(ax)

    # (2) Wild vs. domestic wavefront distance
    ax = axes[1]
    for grp, sub in df["wave_wild"].groupby("group"):
        ax.plot(sub["time"], sub["distance"], lw=3, color=palette_wild[grp], label=grp)
        ax.fill_between(sub["time"], sub["low"], sub["high"], color=fill_wild[grp], alpha=0.7, linewidth=0)
    ax.set_xlim(2000, 2025)
    ax.set_ylim(0, 20000)
    ax.set_xticks(range(2000, 2026, 5))
    ax.set_yticks(range(0, 20001, 5000))
    ax.yaxis.set_major_formatter(FuncFormatter(short_formatter))
    ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.6, axis="y")
    tidy_spines(ax)

    # (3) Host-specific weighted diffusion coefficient
    ax = axes[2]
    for grp, sub in df["diff_host_weighted"].groupby("group"):
        ax.plot(sub["time"], sub["diffusion_coefficient"], lw=3, color=palette_host[grp], label=grp)
        ax.fill_between(sub["time"], sub["low"], sub["high"], color=fill_host[grp], alpha=0.7, linewidth=0)
    ax.set_xlim(2000, 2025)
    ax.set_yscale("log")
    ax.set_ylim(1e2, 3e7)
    ax.set_xticks(range(2000, 2026, 5))
    ax.yaxis.set_major_locator(log_major)
    ax.yaxis.set_minor_locator(log_minor)
    ax.yaxis.set_major_formatter(log_fmt)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.4, alpha=0.6)
    tidy_spines(ax)

    # (4) Wild vs. domestic weighted diffusion coefficient
    ax = axes[3]
    for grp, sub in df["diff_wild_weighted"].groupby("group"):
        ax.plot(sub["time"], sub["diffusion_coefficient"], lw=3, color=palette_wild[grp], label=grp)
        ax.fill_between(sub["time"], sub["low"], sub["high"], color=fill_wild[grp], alpha=0.7, linewidth=0)
    ax.set_xlim(2000, 2025)
    ax.set_yscale("log")
    ax.set_ylim(1e2, 3e7)
    ax.set_xticks(range(2000, 2026, 5))
    ax.yaxis.set_major_locator(log_major)
    ax.yaxis.set_minor_locator(log_minor)
    ax.yaxis.set_major_formatter(log_fmt)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.4, alpha=0.6)
    tidy_spines(ax)

    fig.tight_layout(pad=2.2)

    # Save as SVG
    output_path = pathlib.Path(f"{output_name}.svg")
    fig.savefig(output_path, format="svg", bbox_inches="tight")
    plt.close(fig)