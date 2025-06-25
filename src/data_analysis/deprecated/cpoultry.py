import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, PowerNorm

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['savefig.dpi'] = 600
mpl.rcParams['figure.figsize'] = (10, 6)
mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['xtick.major.width'] = 1.2
mpl.rcParams['ytick.major.width'] = 1.2

def create_heatmap(filepath):
    df = pd.read_csv(filepath)
    
    if 'year' not in df.columns or 'month' not in df.columns:
        raise ValueError("The 'year' or 'month' column is missing in the input file.")
    
    df = df.dropna(subset=['year', 'month'])
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    
    df = df[(df['year'] >= 2004) & (df['year'] <= 2024)]
    
    heatmap_data = df.groupby(['month', 'year']).size().reset_index(name='count')
    
    heatmap_data = heatmap_data.pivot(index='month', columns='year', values='count').fillna(0)
    
    heatmap_data = heatmap_data.reindex(index=range(1, 13), fill_value=0)
    
    heatmap_data = heatmap_data.reindex(columns=range(2004, 2025), fill_value=0)
    
    cmap = LinearSegmentedColormap.from_list(
        'custom_orange', ['#FFF7EC', '#FDBB84', '#E34A33'], N=256)
    
    norm = PowerNorm(gamma=0.5, vmin=0.1, vmax=heatmap_data.values.max())

    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.heatmap(
        heatmap_data,
        cmap=cmap,
        norm=norm,
        linewidths=0.5,
        linecolor='white',
        square=True,
        annot=True,
        fmt=".0f",
        annot_kws={'size': 8, 'color': 'black'},
        cbar_kws={
            'label': 'Number of Events',
            'shrink': 0.8,
            'ticks': mpl.ticker.MaxNLocator(integer=True)
        },
        ax=ax
    )
    
    ax.set_ylabel('Month', fontsize=12, labelpad=10)
    ax.set_xlabel('Year', fontsize=12, labelpad=10)
    ax.set_title('Frequency of Events by Year and Month (Animal Type = Domestic)', fontsize=14, pad=15)
    
    ax.set_yticklabels([f'{m}' for m in range(1, 13)], rotation=0)
    
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    plt.tight_layout()
    
    return fig

try:
    fig = create_heatmap("H7FAO.csv")
    plt.savefig('H7_domestic_heatmap.pdf', bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Error: {e}")