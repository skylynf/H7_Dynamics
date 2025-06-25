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

# ----------------------------------------------
# plotting parameters (unchanged)
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
    计算给定样本的一维 HPD 区间 (Highest Posterior Density)。
    若样本量为 0，返回 (nan, nan)。
    """
    n = len(samples)
    if n == 0:
        return np.nan, np.nan

    sorted_samples = np.sort(samples)
    interval_idx_inc = int(np.floor(cred_mass * n))
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
    处理 GLM 日志文件，提取系数和指示变量数据，
    并计算均值/中位数/CI/HPD 等统计量。
    """
    df = pd.read_csv(file_path, sep='\t', comment='#', low_memory=False)

    df = df[df['state'] != 0]

    activated_coeffs = []

    for i in range(1, 16):
        coeff_col = f'country.coefficients{i}'
        indicator_col = f'country.coefIndicators{i}'

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
    将 HPD 区间及其他统计信息汇总输出到 TSV，并打印到终端。
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

    Path(outfile).write_text(table.to_csv(sep='\t', index=False), encoding='utf-8')
    print("\n===== 95% HPD intervals for all coefficients =====")
    print(table.to_string(index=False, justify='right', float_format='{:,.4f}'.format))
    print(f"\nHPD table written to: {outfile}\n")


def create_combined_plot(activated_coeffs, output_file):
    """
    创建小提琴图 + 散点图组合。
    （代码主体与原来一致，只是读取了新字段，不影响绘图。）
    """
    fig, ax = plt.subplots(figsize=(16, 10))

    plot_data = []
    for coeff in activated_coeffs:
        n = len(coeff['Values'])
        if n == 0:
            continue
        sample_size = min(1000, n)
        indices = np.linspace(0, n - 1, sample_size, dtype=int)
        sampled_values = coeff['Values'][indices]
        for v in sampled_values:
            plot_data.append({
                'Coefficient': coeff['Coefficient'],
                'Value': v,
                'Size': random.uniform(3, 8)
            })

    plot_df = pd.DataFrame(plot_data)

    palette = sns.color_palette("viridis", n_colors=len(activated_coeffs))
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
        ax=ax
    )

    np.random.seed(42)
    jitter = 0.15
    for i, coeff in enumerate(activated_coeffs):
        if coeff['Sample Size'] == 0:
            continue
        coeff_df = plot_df[plot_df['Coefficient'] == coeff['Coefficient']]
        x_pos = i + jitter * (np.random.rand(len(coeff_df)) - 0.5)
        density_gradient = np.linspace(0.2, 0.8, len(coeff_df))
        colors = [plt.cm.viridis(d) for d in density_gradient]
        ax.scatter(
            x_pos,
            coeff_df['Value'],
            s=coeff_df['Size'] * 10,
            c=colors,
            alpha=0.6,
            edgecolors='black',
            linewidths=0.3,
            zorder=10
        )

    for i, coeff in enumerate(activated_coeffs):
        if coeff['Sample Size'] == 0:
            continue
        ax.hlines(coeff['Median'], i - 0.4, i + 0.4,
                  color='red', linewidth=2.5, zorder=20)
        ax.scatter(i, coeff['Mean'], s=120,
                   color='white', edgecolor='black', linewidth=1.5,
                   zorder=30, label='Mean' if i == 0 else "")
        ax.vlines(i, coeff['95% CI Lower'], coeff['95% CI Upper'],
                  color='black', linewidth=2, alpha=0.7, zorder=5)

        activation_pct = coeff['Activation Rate'] * 100
        ax.text(i,
                ax.get_ylim()[0] - 0.15 * np.diff(ax.get_ylim())[0],
                f'{activation_pct:.1f}%\n n={coeff["Sample Size"]:,}',
                ha='center', va='top', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.85,
                          edgecolor='gray', boxstyle='round,pad=0.3'))

    ax.axhline(0, color='#555', linestyle='--', linewidth=2, alpha=0.8)
    ax.set_xlabel('GLM Coefficient', fontsize=14, fontweight='bold')
    ax.set_ylabel('Coefficient Value', fontsize=14, fontweight='bold')
    ax.set_title('Combined Violin and Scatter Plot of GLM Coefficients Posterior Distribution',
                 fontsize=16, fontweight='bold', pad=20)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.3, which='both')

    mean_legend = plt.Line2D([0], [0], marker='o', color='w',
                             markerfacecolor='white', markeredgecolor='black',
                             markersize=10, label='Mean')
    median_legend = plt.Line2D([0], [0], color='red', linewidth=2.5,
                               label='Median')
    ci_legend = plt.Line2D([0], [0], color='black', linewidth=2,
                           alpha=0.7, label='95% CI')
    ax.legend(handles=[mean_legend, median_legend, ci_legend],
              loc='upper right', frameon=True,
              facecolor='white', edgecolor='gray', framealpha=0.9,
              fontsize=11)

    total_points = sum(len(c['Values']) for c in activated_coeffs)
    median_activation = np.median([c['Activation Rate'] for c in activated_coeffs])
    significant_coeffs = sum(
        1 for c in activated_coeffs if c['Sample Size'] > 0 and abs(c['Median']) > 0.5)

    stats_text = (
        f"Global Statistics:\n"
        f"• Total Activated Samples: {total_points:,}\n"
        f"• Median Activation Rate: {median_activation:.1%}\n"
        f"• Significant Coefficients: {significant_coeffs}/15\n"
        f"• Visualization: {len(plot_df):,} points shown (sampled)"
    )
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            ha='left', va='top', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white',
                      alpha=0.9, edgecolor='gray'))

    ax.text(0.98, 0.02,
            "Point color density: █ low → high █",
            transform=ax.transAxes, ha='right', va='bottom',
            fontsize=10, bbox=dict(facecolor='white',
                                   alpha=0.7, edgecolor='none'))

    plt.savefig(output_file, dpi=600)
    plt.close()
    print(f"Figure saved to: {output_file}")
    print(f"Total points visualised: {len(plot_df):,} (sampled)")


def main():
    input_file = "H7glm.country.glm.log"
    output_plot = "GLM_Combined_Violin_Scatter_Plot.png"
    output_hpd = "GLM_Coefficient_HPD.tsv"

    activated_coeffs = process_glm_data(input_file)
    create_combined_plot(activated_coeffs, output_plot)
    export_hpd_table(activated_coeffs, output_hpd)


if __name__ == "__main__":
    main()