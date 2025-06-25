import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, PowerNorm
from matplotlib import patches

mpl.rcParams.update({
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



def create_combined_heatmap(poultry_file, human_file):
    df_poultry = pd.read_csv(poultry_file)
    df_poultry = df_poultry.dropna(subset=['year', 'month'])
    df_poultry['year'] = df_poultry['year'].astype(int)
    df_poultry['month'] = df_poultry['month'].astype(int)
    df_poultry = df_poultry[(df_poultry['year'] >= 2004) & (df_poultry['year'] <= 2024)]
    
    heatmap_p = df_poultry.groupby(['month', 'year']).size().reset_index(name='count')
    heatmap_p = heatmap_p.pivot(index='month', columns='year', values='count').fillna(0)
    heatmap_p = heatmap_p.reindex(index=range(1, 13), columns=range(2004, 2025), fill_value=0)

    df_human = pd.read_excel(human_file)
    df_human['DATE'] = pd.to_datetime(df_human['DATE'], errors='coerce')
    df_human = df_human.dropna(subset=['DATE'])
    df_human['Year'] = df_human['DATE'].dt.year
    df_human['Month'] = df_human['DATE'].dt.month
    df_human = df_human[(df_human['Year'] >= 2004) & (df_human['Year'] <= 2024)]
    
    heatmap_h = df_human.pivot_table(
        index='Month',
        columns='Year',
        values='Event_ID',
        aggfunc='count',
        fill_value=0
    )
    heatmap_h = heatmap_h.reindex(index=range(1, 13), columns=range(2004, 2025), fill_value=0)

    cmap_poultry = LinearSegmentedColormap.from_list('green', ["#f0f9e889", '#7bccc4', '#0868ac'], N=256)
    cmap_human = LinearSegmentedColormap.from_list('orange', ["#fee6ce75", '#fd8d3c', '#bd0026'], N=256)
    norm_p = PowerNorm(gamma=0.35, vmin=0.1, vmax=heatmap_p.max().max())
    norm_h = PowerNorm(gamma=0.35, vmin=0.1, vmax=heatmap_h.max().max())

    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_facecolor('white')

    cell_width = 0.9
    cell_height = 0.85

    season_order = [6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7]

    for month in range(1, 13):
        for year in range(2004, 2025):
            y_idx = season_order.index(month)
            x_idx = year - 2004

            rect_left = patches.Rectangle(
                (x_idx, y_idx),
                width=cell_width / 2,
                height=cell_height,
                facecolor=cmap_poultry(norm_p(heatmap_p.loc[month, year])),
                edgecolor='none',
                zorder=2
            )
            ax.add_patch(rect_left)

            rect_right = patches.Rectangle(
                (x_idx + cell_width / 2, y_idx),
                width=cell_width / 2,
                height=cell_height,
                facecolor=cmap_human(norm_h(heatmap_h.loc[month, year])),
                edgecolor='none',
                zorder=2
            )
            ax.add_patch(rect_right)


    ax.set_xlim(-3.5, 21.5)
    ax.set_ylim(0, 12.5)
    ax.invert_yaxis()
    
    ax.set_xticks(np.arange(0.5, 21, 2))
    ax.set_xticklabels(range(2004, 2025, 2))
    
    ax.set_yticks(np.arange(0.5, 12.5, 1))
    ax.set_yticklabels([
        'Jun', 'May', 'Apr', 'Mar', 'Feb', 'Jan',
        'Dec', 'Nov', 'Oct', 'Sep', 'Aug', 'Jul'
    ])

    ax.grid(False)


    cax1 = fig.add_axes([0.08, 0.14, 0.025, 0.75])
    cbar1 = plt.colorbar(plt.cm.ScalarMappable(norm=norm_p, cmap=cmap_poultry),
                        cax=cax1, orientation='vertical')
    cbar1.ax.tick_params(size=0, labelsize=14)
    cbar1.outline.set_visible(False)

    cax2 = fig.add_axes([0.138, 0.14, 0.025, 0.75])
    cbar2 = plt.colorbar(plt.cm.ScalarMappable(norm=norm_h, cmap=cmap_human),
                        cax=cax2, orientation='vertical')
    cbar2.ax.tick_params(size=0, labelsize=14)
    cbar2.outline.set_visible(False)

    cbar1.ax.text(1, 1.02, 'Poultry', 
                transform=cbar1.ax.transAxes,
                ha='center', va='bottom',
                fontsize=14, color='black', weight='bold')

    cbar2.ax.text(1, 1.02, 'Human',
                transform=cbar2.ax.transAxes,
                ha='center', va='bottom',
                fontsize=14, color='black', weight='bold')

    poultry_ticks = [0,  25, 50, 100,200]
    human_ticks = [0,  10, 20, 40, 80,160]
    cbar1.set_ticks(poultry_ticks)
    cbar2.set_ticks(human_ticks)
    

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout(pad=3.0)
    return fig

try:
    fig = create_combined_heatmap("data/H7FAO.csv", "data/H7_human_infection.xlsx")
    # plt.savefig('Modified_Heatmap.pdf', bbox_inches='tight', dpi=600)
    # save as SVG
    plt.savefig('Modified_Heatmap.svg', format='svg', bbox_inches='tight', dpi=600)
    plt.show()
except Exception as e:
    print(f"Error: {e}")