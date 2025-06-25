#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone legend figure for Fig. 7
author: your-name
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# corresponding to the main figure, this legend is designed to match the color scheme and style
# ---------------------------------------------------------------------
# Global Aesthetic Parameters
# use arial
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

palette_host = {"Anseriformes": "black", "Galliformes": "red"}
fill_host    = {"Anseriformes": "#abddff", "Galliformes": "#ffc2c2"}
palette_Wild = {"Wild": "purple", "Domestic": "orange"}
fill_Wild    = {"Wild": "#dab5ff", "Domestic": "#ffd9b3"}

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
handles = []
labels  = []

# host-specific wavefront
for grp in ["Anseriformes", "Galliformes"]:
    handles.append(Line2D([0], [0], color=palette_host[grp], lw=2))
    handles.append(Patch(facecolor=fill_host[grp], edgecolor="none", alpha=0.5))
    labels.extend([f"{grp} ", f"{grp} 95% HPD"])

# Wild/Domestic wavefront
for grp in ["Wild", "Domestic"]:
    handles.append(Line2D([0], [0], color=palette_Wild[grp], lw=2))
    handles.append(Patch(facecolor=fill_Wild[grp], edgecolor="none", alpha=0.5))
    labels.extend([f"{grp.capitalize()} ", f"{grp.capitalize()} 95% HPD"])

fig_legend = plt.figure(figsize=(6, 1.6))
fig_legend.legend(handles, labels, ncol=4, frameon=False,
                  loc="center", columnspacing=1.2, handletextpad=0.6)
fig_legend.tight_layout()

fig_legend.savefig("fig7_legend_only.pdf", bbox_inches="tight")
fig_legend.savefig("fig7_legend_only.png", dpi=600, bbox_inches="tight")
fig_legend.savefig("fig7_legend_only.svg", bbox_inches="tight")
# plt.show()