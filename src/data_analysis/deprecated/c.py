import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, PowerNorm
import calendar

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['savefig.dpi'] = 600
mpl.rcParams['figure.figsize'] = (8, 5)
mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['xtick.major.width'] = 1.2
mpl.rcParams['ytick.major.width'] = 1.2

def create_heatmap(filepath):
    df = pd.read_excel(filepath)
    
    if 'DATE' not in df.columns:
        raise ValueError("The 'DATE' column is missing in the input file.")
    
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    if df['DATE'].isnull().any():
        print("Warning: Some 'DATE' values could not be parsed and were set to NaT.")
    
    df = df.dropna(subset=['DATE'])
    
    df['Year'] = df['DATE'].dt.year
    df['Month'] = df['DATE'].dt.month
    
    df = df[(df['Year'] >= 2004) & (df['Year'] <= 2024)]
    
    df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
    
    if 'Country' not in df.columns:
        raise ValueError("The 'Country' column is missing in the input file.")
    
    heatmap_data = df.pivot_table(
        index='Month',
        columns='Year',
        values='Country',
        aggfunc='count',
        fill_value=0
    ).reindex(calendar.month_abbr[1:])
    
    all_years = list(range(2004, 2025))
    heatmap_data = heatmap_data.reindex(columns=all_years, fill_value=0)
    
    cmap = LinearSegmentedColormap.from_list(
        'custom_orange', ['#FFF7EC', '#FDBB84', '#E34A33'], N=256)
    
    norm = PowerNorm(gamma=0.5, vmin=0.1, vmax=heatmap_data.values.max())

    fig, ax = plt.subplots()
    
    sns.heatmap(
        heatmap_data,
        cmap=cmap,
        norm=norm,
        linewidths=0.5,
        linecolor='white',
        square=True,
        annot=True,
        fmt="d",
        annot_kws={'size': 8, 'color': 'black'},
        cbar_kws={
            'label': 'Number of Cases',
            'shrink': 0.8,
            'ticks': mpl.ticker.MaxNLocator(integer=True)
        },
        ax=ax
    )
    
    ax.set_ylabel('Month', fontsize=10, labelpad=10)
    ax.set_xlabel('Year', fontsize=10, labelpad=10)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=8)
    cbar.ax.yaxis.label.set_size(10)
    
    ax.tick_params(axis='both', which='major', labelsize=8, 
                   rotation=0, colors='black')
    plt.tight_layout()
    
    return fig

try:
    fig = create_heatmap("H7N9人感染.xlsx")
    plt.savefig('H7N9_epidemiological_heatmap_12months.pdf', bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Error: {e}")