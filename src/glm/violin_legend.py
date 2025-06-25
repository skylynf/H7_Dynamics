#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate legend for violin plot visualization.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# ----------------------------------------------
# plotting parameters
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 12,
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': 'black',
    'axes.labelcolor': 'black',
    'xtick.color': 'black',
    'ytick.color': 'black',
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'savefig.transparent': False,
    'figure.dpi': 300,
    'figure.autolayout': True
})
# ----------------------------------------------


def create_legend():
    """
    Create a separate legend figure for the violin plot visualization.
    """
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    
    mean_legend = plt.Line2D([0], [0], marker='o', color='w',
                            markerfacecolor='white', markeredgecolor='black',
                            markersize=8, label='Mean')
    median_legend = plt.Line2D([0], [0], color='#D62728', linewidth=2.5,
                              label='Median')
    hpd_legend = plt.Line2D([0], [0], color='#1F77B4', linewidth=2.5,
                           alpha=0.9, label='95% HPD')
    
    cmap = plt.cm.get_cmap('plasma')
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    legend = ax.legend(handles=[mean_legend, median_legend, hpd_legend],
                      loc='center', frameon=True,
                      facecolor='white', edgecolor='black',
                      framealpha=1.0, fontsize=12)
    
    cbar = fig.colorbar(sm, ax=ax, fraction=0.1, pad=0.1)
    cbar.set_label('Point Density', fontsize=12, color='black')
    cbar.ax.tick_params(labelsize=10, colors='black')
    
    ax.set_axis_off()
    
    plt.savefig('violin_legend.png', dpi=600)
    plt.savefig('violin_legend.svg', dpi=600)
    plt.close()
    print("Legend saved as violin_legend.png and violin_legend.svg")


if __name__ == "__main__":
    create_legend() 