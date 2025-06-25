#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Combined violin + scatter visualisation for GLM coefficients
and extraction of 95 % HPD intervals.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker
import random
from pathlib import Path
import matplotlib as mpl

# ----------------------------------------------
# plotting parameters
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 12,
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': '.4',
    'axes.labelcolor': '.15',
    'axes.titlepad': 15,
    'axes.grid': True,
    'grid.color': '.92',
    'grid.linewidth': 1,
    'legend.frameon': False,
    'legend.facecolor': 'white',
    'legend.loc': 'best',
    'xtick.bottom': True,
    'ytick.left': True,
    'xtick.color': '.4',
    'ytick.color': '.4',
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'savefig.transparent': False,
    'figure.dpi': 300,
    'figure.autolayout': True
})
# ----------------------------------------------


def compute_hpd(samples: np.ndarray, cred_mass: float = 0.95):
    """
    Calculate the 1D HPD interval (Highest Posterior Density) for given samples.
    Returns (nan, nan) if sample size is 0.
    """
    n = len(samples)
    if n == 0:
        return np.nan, np.nan

    sorted_samples = np.sort(samples)
    interval_idx_inc = int(np.floor(cred_mass * n))
    # Fallback to regular quantiles if insufficient samples
    if interval_idx_inc < 1:
        return np.percentile(samples, [(1 - cred_mass) / 2 * 100,
                                       (1 + cred_mass) / 2 * 100])

    interval_width = sorted_samples[interval_idx_inc:] - sorted_samples[: n - interval_idx_inc]
    min_idx = np.argmin(interval_width)
    hpd_min = sorted_samples[min_idx]
    hpd_max = sorted_samples[min_idx + interval_idx_inc]
    return hpd_min, hpd_max


def process_glm_data(file_path):
    """
    Process GLM log file to extract coefficients and indicator variables,
    and calculate statistics like mean/median/CI/HPD.
    """
    # Read data, skipping comment lines
    df = pd.read_csv(file_path, sep='\t', comment='#', low_memory=False)

    # Remove initial state rows (state=0)
    df = df[df['state'] != 0]

    max_coef = 0
    for i in range(1, 16):
        if f'country.coefficients{i}' in df.columns:
            max_coef = i
        else:
            break

    print(f"检测到 {max_coef} 个系数")

    # Prepare results storage
    activated_coeffs = []

    for i in range(1, max_coef + 1):
        coeff_col = f'country.coefficients{i}'
        indicator_col = f'country.coefIndicators{i}'

        # Activation mask
        activated_mask = df[indicator_col] == 1.0
        activated_values = df.loc[activated_mask, coeff_col].to_numpy()
        n_activated = len(activated_values)

        if n_activated > 0:
            mean_val = activated_values.mean()
            median_val = np.median(activated_values)
            std_val = activated_values.std()
            ci_lower, ci_upper = np.percentile(activated_values, [2.5, 97.5])
            hpd_lower, hpd_upper = compute_hpd(activated_values, 0.95)
        else:
            mean_val = median_val = std_val = np.nan
            ci_lower = ci_upper = hpd_lower = hpd_upper = np.nan

        activated_coeffs.append({
            'Coefficient': f'β{i}',
            'Values': activated_values,
            'Activation Rate': n_activated / len(df),
            'Mean': mean_val,
            'Median': median_val,
            'Std': std_val,
            '95% CI Lower': ci_lower,
            '95% CI Upper': ci_upper,
            'HPD Lower': hpd_lower,
            'HPD Upper': hpd_upper,
            'Sample Size': n_activated
        })

    return activated_coeffs


def export_hpd_table(activated_coeffs, outfile="GLM_Coefficient_HPD.tsv"):
    """
    Export HPD intervals and other statistics to TSV and print to console.
    """
    table = pd.DataFrame([
        {
            'Coefficient': c['Coefficient'],
            'Sample Size': c['Sample Size'],
            'Activation Rate (%)': f"{c['Activation Rate'] * 100:.1f}",
            'Mean': c['Mean'],
            'Median': c['Median'],
            'Std': c['Std'],
            '95% CI Lower': c['95% CI Lower'],
            '95% CI Upper': c['95% CI Upper'],
            'HPD Lower': c['HPD Lower'],
            'HPD Upper': c['HPD Upper']
        }
        for c in activated_coeffs
    ])

    # Save to file
    Path(outfile).write_text(table.to_csv(sep='\t', index=False), encoding='utf-8')
    print("\n===== 95% HPD intervals for all coefficients =====")
    print(table.to_string(index=False, justify='right', float_format='{:,.4f}'.format))
    print(f"\nHPD table written to: {outfile}\n")


def create_combined_plot(activated_coeffs, output_file):
    """
    Create combined violin + scatter plot using HPD intervals and density-based coloring.
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.1)
    
    ax = fig.add_subplot(gs[0])
    ax_bar = fig.add_subplot(gs[1])

    # ---------- Assemble plot data with density-based coloring ----------
    plot_data = []
    all_values = np.array([])  # Collect all values for global density calculation
    
    for coeff in activated_coeffs:
        n = len(coeff['Values'])
        if n == 0:
            continue
        sample_size = min(1500, n)
        indices = np.linspace(0, n - 1, sample_size, dtype=int)
        sampled_values = coeff['Values'][indices]
        all_values = np.concatenate((all_values, sampled_values))
        
        for v in sampled_values:
            plot_data.append({
                'Coefficient': coeff['Coefficient'],
                'Value': v,
                'Size': random.uniform(2, 5)  # Smaller point size
            })

    plot_df = pd.DataFrame(plot_data)
    
    # Calculate global density for consistent coloring across coefficients
    if len(all_values) > 1:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(all_values)
        plot_df['Density'] = kde(plot_df['Value'])
        # Normalize densities to [0, 1]
        plot_df['Density'] = (plot_df['Density'] - plot_df['Density'].min()) / \
                             (plot_df['Density'].max() - plot_df['Density'].min())
    else:
        plot_df['Density'] = 0.5

    np.random.seed(42)
    jitter = 0.15
    
    # Create a colormap for density (blue to purple)
    cmap = plt.cm.get_cmap('plasma')
    
    for i, coeff in enumerate(activated_coeffs):
        if coeff['Sample Size'] == 0:
            continue
        coeff_df = plot_df[plot_df['Coefficient'] == coeff['Coefficient']]
        x_pos = i + jitter * (np.random.rand(len(coeff_df)) - 0.5)
        
        # Map density to colors
        colors = cmap(coeff_df['Density'])
        
        ax.scatter(
            x_pos,
            coeff_df['Value'],
            s=coeff_df['Size'] * 20,
            c=colors,
            alpha=0.5,
            edgecolors='none',
            zorder=5
        )

    palette = sns.color_palette("crest", n_colors=len(activated_coeffs))
    sns.violinplot(
        x='Coefficient',
        y='Value',
        data=plot_df,
        palette=palette,
        inner=None,
        cut=0,
        bw_method=0.25,
        linewidth=1.5,
        saturation=0.85,
        width=1.2,
        alpha=0.7,
        ax=ax,
        zorder=10
    )

    for i, coeff in enumerate(activated_coeffs):
        if coeff['Sample Size'] == 0:
            continue
        # Median line
        ax.hlines(coeff['Median'], i - 0.4, i + 0.4,
                  color='#D62728', linewidth=2.5, zorder=20)
        
        # Mean marker
        ax.scatter(i, coeff['Mean'], s=100,
                   color='white', edgecolor='black', linewidth=1.5,
                   zorder=30, label='Mean' if i == 0 else "")
        
        # HPD interval
        ax.vlines(i, coeff['HPD Lower'], coeff['HPD Upper'],
                  color='#1F77B4', linewidth=2.5, alpha=0.9, zorder=15)

    ax.axhline(0, color='#555', linestyle='--', linewidth=2, alpha=0.8)
    ax.set_xlabel('')
    ax.set_ylabel('Coefficient Value', fontsize=14, fontweight='bold')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.3, which='both')

    mean_legend = plt.Line2D([0], [0], marker='o', color='w',
                             markerfacecolor='white', markeredgecolor='black',
                             markersize=8, label='Mean')
    median_legend = plt.Line2D([0], [0], color='#D62728', linewidth=2.5,
                               label='Median')
    hpd_legend = plt.Line2D([0], [0], color='#1F77B4', linewidth=2.5,
                            alpha=0.9, label='95% HPD')
    ax.legend(handles=[mean_legend, median_legend, hpd_legend],
              loc='upper right', frameon=True,
              facecolor='white', edgecolor='gray', framealpha=0.9,
              fontsize=11)

    coeff_names = [c['Coefficient'] for c in activated_coeffs]
    activation_rates = [c['Activation Rate'] * 100 for c in activated_coeffs]
    
    bars = ax_bar.bar(coeff_names, activation_rates, 
                      color=palette, alpha=0.7)
    
    for bar in bars:
        height = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=10)
    
    ax_bar.set_ylabel('Activation Rate (%)', fontsize=12)
    ax_bar.set_ylim(0, 105)
    ax_bar.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax_bar.tick_params(axis='x', rotation=45)
    
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.02, pad=0.01)
    cbar.set_label('Point Density', fontsize=10)
    cbar.ax.tick_params(labelsize=9)

    plt.savefig(output_file, dpi=600)
    plt.close()
    print(f"Figure saved to: {output_file}")
    print(f"Total points visualised: {len(plot_df):,}")


def main():
    input_files = [
        "H7glm.country.glm.log",
        "nosample_H7glm.country.glm.log"
    ]
    
    for input_file in input_files:
        base_name = input_file.replace(".log", "")
        
        output_plot_png = f"{base_name}_violin_plot.png"
        output_plot_svg = f"{base_name}_violin_plot.svg"
        output_hpd = f"{base_name}_HPD.tsv"

        print(f"\n处理文件: {input_file}")
        activated_coeffs = process_glm_data(input_file)
        
        create_combined_plot(activated_coeffs, output_plot_png)
        create_combined_plot(activated_coeffs, output_plot_svg)
        
        export_hpd_table(activated_coeffs, output_hpd)
        
        print(f"完成处理: {input_file}")
        print(f"生成的文件:")
        print(f"- {output_plot_png}")
        print(f"- {output_plot_svg}")
        print(f"- {output_hpd}")


if __name__ == "__main__":
    main()