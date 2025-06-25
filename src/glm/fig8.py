import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import matplotlib.gridspec as gridspec

# =====================
# NATURE STYLE SETTINGS
# =====================
plt.rcParams.update({
    'font.sans-serif': 'Arial',
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.dpi': 600,
    'figure.figsize': (7.2, 4.5),
    'axes.linewidth': 0.6,
    'grid.linewidth': 0.5,
    'lines.linewidth': 1.0,
    'hatch.linewidth': 0.3,
})

# ======================
# ======================
coeff_df = pd.read_excel("GLMresult2.xlsx", sheet_name="coefficient")
prob_df = pd.read_excel("GLMresult2.xlsx", sheet_name="inclusionprobability")

coeff_df['Indicator'] = coeff_df['Indicator'].replace({
    'air passenger origin': 'Air Passenger (o)',
    'air passenger destination': 'Air Passenger (d)',
    'chickenstock origin': 'Chicken Stock (o)',
    'chickenstock destination': 'Chicken Stock (d)',
    'GDPper origin': 'GDP Per Capita (o)',
    'GDPper destination': 'GDP Per Capita (d)',
    'rainfall origin': 'Rainfall (o)',
    'rainfall destination': 'Rainfall (d)',
    'migration': 'Migration',
    'trade weight': 'Trade Weight',
    'temperature origin': 'Temperature (o)',
    'temperature destination': 'Temperature (d)',
    'sample size origin': 'Sample Size (o)',
    'sample size destination': 'Sample Size (d)',
    'distance': 'Distance'
})

prob_df['Indicator'] = prob_df['Indicator'].replace({
    'air passenger origin': 'Air Passenger (o)',
    'air passenger destination': 'Air Passenger (d)',
    'chickenstock origin': 'Chicken Stock (o)',
    'chickenstock destination': 'Chicken Stock (d)',
    'GDPper origin': 'GDP Per Capita (o)',
    'GDPper destination': 'GDP Per Capita (d)',
    'rainfall origin': 'Rainfall (o)',
    'rainfall destination': 'Rainfall (d)',
    'migration': 'Migration',
    'trade weight': 'Trade Weight',
    'temperature origin': 'Temperature (o)',
    'temperature destination': 'Temperature (d)',
    'sample size origin': 'Sample Size (o)',
    'sample size destination': 'Sample Size (d)',
    'distance': 'Distance'
})

# ==========================
# ==========================
fig = plt.figure(constrained_layout=True, figsize=(7.2, 4.5))
gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.2, 1])

# ----------------------
# ----------------------
ax1 = fig.add_subplot(gs[0])
coeff_df = coeff_df.sort_values('Coefficient', ascending=False)

ax1.hlines(y=range(len(coeff_df)), 
           xmin=coeff_df['HPD_lower'],  
           xmax=coeff_df['HPD_upper'],
           color='#004466', 
           linewidth=1.2,
           alpha=0.7)

ax1.scatter(coeff_df['Coefficient'], 
            range(len(coeff_df)), 
            color='#0072B2', 
            s=24,
            zorder=3,
            alpha=0.9)

ax1.axvline(0, color='#D55E00', linestyle='--', linewidth=1.0, alpha=0.8)

ax1.set_yticks(range(len(coeff_df)))
ax1.set_yticklabels(coeff_df['Indicator'])
ax1.set_xlabel('Coefficient Estimate', fontweight='bold', labelpad=2)
ax1.set_ylabel('')

# --------------------------
# --------------------------
ax2 = fig.add_subplot(gs[1])

prob_df = prob_df.set_index('Indicator').reindex(coeff_df['Indicator']).reset_index()

bars = ax2.barh(range(len(prob_df)), 
                prob_df['inclusion_probability'],
                color='#69b3a2',
                height=0.6,
                edgecolor='white',
                linewidth=0.5)

for i, bar in enumerate(bars):
    width = bar.get_width()
    if not pd.isna(width):
        ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2, 
                 f'{width:.2f}', 
                 ha='left', va='center',
                 fontsize=6)

ax2.set_xlim(0, 1.1)
ax2.set_xlabel('Inclusion Probability', fontweight='bold', labelpad=2)
ax2.set_ylabel('')
ax2.set_yticks(range(len(prob_df)))
ax2.set_yticklabels([])
# ax2.set_yticklabels(prob_df['Indicator'])

plt.tight_layout(pad=2.0)
plt.subplots_adjust(wspace=0.4)

# ======================
# ======================
plt.savefig('GLM_Analysis_Nature.svg', 
            dpi=600,
            bbox_inches='tight',
            pad_inches=0.05,
            format='svg')

plt.savefig('GLM_Analysis_Nature.pdf',
            bbox_inches='tight',
            pad_inches=0.05)

plt.show()