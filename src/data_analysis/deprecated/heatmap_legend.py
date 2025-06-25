import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, PowerNorm

plt.rcParams.update({
    'font.family': 'Arial',
    'savefig.dpi': 600,
    # 'figure.figsize': (16, 9),
    'axes.linewidth': 2,
    'xtick.major.width': 2,
    'ytick.major.width': 2,
    'axes.labelsize': 14,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'axes.titlesize': 14
})


cmap_poultry = LinearSegmentedColormap.from_list('green', ["#f0f9e889", '#7bccc4', '#0868ac'], N=256)
cmap_human = LinearSegmentedColormap.from_list('orange', ["#fee6ce75", '#fd8d3c', '#bd0026'], N=256)
norm_p = PowerNorm(gamma=0.35, vmin=0.1, vmax=100)
norm_h = PowerNorm(gamma=0.35, vmin=0.1, vmax=50)

fig = plt.figure(figsize=(2, 10), facecolor='none')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

cax1 = fig.add_axes([0.1, 0.2, 0.2, 0.6])
cbar1 = plt.colorbar(plt.cm.ScalarMappable(norm=norm_p, cmap=cmap_poultry),
                     cax=cax1, orientation='vertical')
cbar1.ax.tick_params(size=0, labelsize=14)
cbar1.outline.set_visible(False)

cax2 = fig.add_axes([0.5, 0.2, 0.2, 0.6])
cbar2 = plt.colorbar(plt.cm.ScalarMappable(norm=norm_h, cmap=cmap_human),
                     cax=cax2, orientation='vertical')
cbar2.ax.tick_params(size=0, labelsize=14)
cbar2.outline.set_visible(False)

cbar1.ax.text(0.5, 1.05, 'Poultry', 
             transform=cbar1.ax.transAxes,
             ha='center', va='bottom',
             fontsize=14, color='black', weight='bold')

cbar2.ax.text(0.5, 1.05, 'Human',
             transform=cbar2.ax.transAxes,
             ha='center', va='bottom',
             fontsize=14, color='black', weight='bold')


#show

plt.savefig('Combined_Legend_Nature.svg', format='svg', 
            bbox_inches='tight', pad_inches=0.1,
            transparent=True)

plt.show()
plt.close()