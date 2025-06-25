#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Symmetric (Centered) Ridge-like plot for temporal distribution of H7 sub-types.
Changes:
1. Unified H7, H7N8, and H7N4/5/6 into a single category "Other H7".
2. Thickened all edge lines for better visual separation.
3. Fixed scale legend to show varying line widths corresponding to the scale values.
4. Added x-axis ticks with short lines.
5. Extended the x-axis slightly beyond the leftmost and rightmost data points.
6. Added yticks with short lines and converted labels to absolute values.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from matplotlib.patches import Patch
import matplotlib as mpl

try:
    df = pd.read_csv("./data/序列亚型堆叠图.csv")
    if not {'year', 'subtype'}.issubset(df.columns):
        raise ValueError("输入数据必须包含 'year' 和 'subtype' 列")
except Exception as e:
    raise RuntimeError(f"数据读取或验证失败: {e}")

# Combine H7, H7N8, and H7N4/5/6 into a single category
df['subtype'] = df['subtype'].replace({
    'H7': 'Other H7',
    'H7N8': 'Other H7',
    'H7N4': 'Other H7',
    'H7N5': 'Other H7',
    'H7N6': 'Other H7'
})

frequency = (
    df.groupby(['year', 'subtype'])
      .size()
      .reset_index(name='count')  # ← Raw count, no log-compression
)

wide_df = (
    frequency
    .pivot(index='year', columns='subtype', values='count')
    .fillna(0)
)

wide_df.index = wide_df.index.astype(int)
all_years = np.arange(wide_df.index.min(), wide_df.index.max() + 1)
wide_df = wide_df.reindex(all_years, fill_value=0)

def safe_spline_interp(series, x_grid, s_factor=0.8):
    """
    Spline / linear interpolation on a common grid.
    Returns y values aligned with x_grid (np.ndarray).
    """
    x = series.index.astype(float).values
    y = series.values.astype(float)
    valid = y > 0
    x_valid, y_valid = x[valid], y[valid]

    y_new = np.zeros_like(x_grid)
    if len(x_valid) == 0:
        return y_new
    if len(x_valid) == 1:                       # single point → nearest
        y_new[np.abs(x_grid - x_valid[0]).argmin()] = y_valid[0]
        return y_new

    x_start, x_end = x_valid.min(), x_valid.max()
    mask = (x_grid >= x_start) & (x_grid <= x_end)

    k = min(3, len(x_valid) - 1)
    s = s_factor * np.sqrt(len(x_valid)) if len(x_valid) > 2 else 0
    try:
        spline = UnivariateSpline(x_valid, y_valid, k=k, s=s)
        y_new[mask] = spline(x_grid[mask])
    except Exception:                            # fallback → linear
        y_new[mask] = np.interp(x_grid[mask], x_valid, y_valid)

    y_new[y_new < 0] = 0
    return y_new

# Nature’s preferred 10-colour qualitative scheme
nature_palette = [
    "#1b9e77", "#66a61e", "#7570b3", "#e7298a", "#d95f02",
     "#666666", "#a6cee3", "#fb9a99"
]
subtypes_sorted = sorted(wide_df.columns)
subtype_colors = {st: nature_palette[i % len(nature_palette)]
                  for i, st in enumerate(subtypes_sorted)}

num_points = 400            # smoother curves
x_grid = np.linspace(wide_df.index.min(), wide_df.index.max(), num_points)

ys, labels, colors = [], [], []
for st in subtypes_sorted:
    y_interp = safe_spline_interp(wide_df[st], x_grid, s_factor=1.2)
    if y_interp.max() == 0:
        continue
    ys.append(y_interp)
    labels.append(st)
    colors.append(subtype_colors[st])

ys = np.array(ys)                    # shape → (n_subtype, num_points)
total_y = ys.sum(axis=0)
baseline = -total_y / 2              # symmetry around y = 0

mpl.rcParams.update({
    'font.family': 'Arial',
    'savefig.dpi': 600,
    'figure.figsize': (12, 5),
    'axes.linewidth': 2,
    'xtick.major.width': 2,
    'ytick.major.width': 2,
    'axes.labelsize': 16,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'axes.titlesize': 16
})

fig, ax = plt.subplots(figsize=(15, 6))

bottom = baseline.copy()
for y_layer, st, c in zip(ys, labels, colors):
    ax.fill_between(
        x_grid, bottom, bottom + y_layer,
        color=c, linewidth=0, alpha=0.88
    )
    ax.plot(x_grid, bottom + y_layer, color='black', linewidth=1.2)
    ax.plot(x_grid, bottom, color='black', linewidth=1.2)
    bottom += y_layer

x_min, x_max = wide_df.index.min(), wide_df.index.max() + 1
ax.set_xlim(x_min, x_max)
ax.set_xticks(np.arange(wide_df.index.min(), wide_df.index.max() + 1, 2))
ax.tick_params(axis='x', which='both', length=6)

ax.set_ylim(baseline.min() * 1.1, (baseline + total_y).max() * 1.1)

# Add yticks with absolute value labels
ytick_values = np.linspace(-300, 300, 7)
ytick_labels = [f"{int(abs(y))}" for y in ytick_values]
ax.set_yticks(ytick_values)
ax.set_yticklabels(ytick_labels)
ax.tick_params(axis='y', which='both', length=6)

# keep only bottom and left spines
for name, spine in ax.spines.items():
    spine.set_visible(name == "bottom" or name == "left")
    if name in ["bottom", "left"]:
        spine.set_linewidth(2)

handles_sub = [
    Patch(facecolor=c, edgecolor='black', linewidth=1, label=st) for st, c in zip(labels, colors)
]

leg1 = ax.legend(
    handles=handles_sub, title="Subtype", frameon=False,
    loc='upper left', bbox_to_anchor=(0.05, 1.05), fontsize=14,
    title_fontsize=16,
    ncol=2
)

# Save to SVG and PNG
plt.savefig("subtypes.svg", dpi=600, bbox_inches="tight", transparent=False)
plt.tight_layout()
plt.show()