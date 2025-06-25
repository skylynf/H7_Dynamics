import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from matplotlib.patches import Patch

try:
    df = pd.read_csv("序列亚型堆叠图.csv")
    if not {'year', 'subtype'}.issubset(df.columns):
        raise ValueError("输入数据必须包含 'year' 和 'subtype' 列")
except Exception as e:
    raise RuntimeError(f"数据读取或验证失败: {e}")

frequency = df.groupby(['year', 'subtype']).size().reset_index(name='count')
wide_df = frequency.pivot(index='year', columns='subtype', values='count').fillna(0)

wide_df.index = wide_df.index.astype(int)
all_years = np.arange(wide_df.index.min(), wide_df.index.max() + 1)
wide_df = wide_df.reindex(all_years, fill_value=0)

def safe_spline_interp(data, num_points=300, s_factor=0.8):
    x = data.index.values.astype(float)
    y = data.values.astype(float)
    
    valid_mask = y > 0
    valid_x = x[valid_mask]
    valid_y = y[valid_mask]
    
    if len(valid_x) < 2:
        return x, np.zeros_like(x)
    
    x_start = valid_x.min()
    x_end = valid_x.max()
    
    x_new = np.linspace(x.min(), x.max(), num_points)
    y_new = np.zeros_like(x_new)
    
    if len(valid_x) > 1:
        s = s_factor * np.sqrt(len(valid_x)) if len(valid_x) > 2 else 0
        k = min(3, len(valid_x) - 1)
        
        try:
            spline = UnivariateSpline(valid_x, valid_y, k=k, s=s)
            interp_mask = (x_new >= x_start) & (x_new <= x_end)
            y_new[interp_mask] = spline(x_new[interp_mask])
        except:
            y_new[interp_mask] = np.interp(x_new[interp_mask], valid_x, valid_y)
    
    y_new[y_new < 0] = 0
    y_new[x_new < x_start] = 0
    y_new[x_new > x_end] = 0
    
    return x_new, y_new

subtype_colors = {
    'H7': '#808080',    'H7N1': '#006d2c',  'H7N2': '#1f77b4',
    'H7N3': '#d62728',  'H7N4': '#9467bd',  'H7N5': '#8c564b',
    'H7N6': '#f7e715',  'H7N7': '#e377c2',  'H7N8': '#2ca02c',
    'H7N9': '#ff7f0e'
}

# plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

bottom = np.zeros(300)
for st in sorted(wide_df.columns):
    if st not in subtype_colors:
        continue
    
    x_smooth, y_smooth = safe_spline_interp(wide_df[st], s_factor=1.2)
    ax.fill_between(x_smooth, bottom, bottom + y_smooth,
                    color=subtype_colors[st],
                    edgecolor='black',
                    linewidth=0.8,
                    alpha=0.85)
    bottom += y_smooth

ax.set_xlim(wide_df.index.min(), wide_df.index.max())
ax.set_xticks(np.arange(wide_df.index.min(), wide_df.index.max() + 1, 2))
ax.tick_params(axis='both', which='major', width=1.5)

handles = [Patch(facecolor=subtype_colors[st], edgecolor='black', label=st) 
           for st in wide_df.columns if st in subtype_colors]
ax.legend(handles=handles,
          loc='upper left',
          bbox_to_anchor=(1.02, 1),
          title='Subtype',
          frameon=True)

ax.set_xlabel('Year', fontweight='bold', labelpad=10)
ax.set_ylabel('Number of Sequences', fontweight='bold', labelpad=10)
ax.set_title('Controlled Smoothing of H7 Subtype Temporal Distribution',
             fontsize=14, pad=20, fontweight='bold')

for spine in ax.spines.values():
    spine.set_linewidth(1.5)
    spine.set_color('black')

plt.tight_layout()
plt.savefig('controlled_smoothing_H7_subtypes.png', bbox_inches='tight', dpi=300)
plt.show()