import matplotlib.pyplot as plt
import pandas as pd

DATA_CONFIG = {
    'H7': {
        'regions': ["Africa", "Asia", "Europe", "North America", "South America"],
        'values': [62.908, 558.194, 349.981, 275.364, 62.908]
    },
    'H7N3': {
        'regions': ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"],
        'values': [11.95, 280.213, 160.476, 456.726, 12.922, 98.636]
    },
    'H7N7': {
        'regions': ["Africa", "Asia", "Europe", "North America", "Oceania"],
        'values': [47.46, 340.604, 279.129, 50.824, 15.704]
    },
    'H7N9': {
        'regions': ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"],
        'values': [9.778, 434.609, 68.409, 119.438, 33.663, 30.835]
    }
}

REGION_COLORS = {
    'Africa': '#4E79A7',
    'Asia': '#F28E2B',
    'Europe': '#59A14F',
    'North America': '#E15759',
    'South America': '#B07AA1',
    'Oceania': '#FF9DA7'
}

def visualize_virus_data(subtype='H7', plot_type='donut'):
    """参数化可视化函数
    
    Args:
        subtype (str): 病毒亚型 (H7, H7N3, H7N7, H7N9)
        plot_type (str): 可视化类型 (donut, bar)
    """
    data = DATA_CONFIG.get(subtype)
    if not data:
        raise ValueError(f"Invalid subtype: {subtype}")
    
    df = pd.DataFrame({
        'Region': data['regions'],
        'Value': data['values']
    })
    total = df['Value'].sum()
    df['Percentage'] = df['Value'] / total * 100
    
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.size': 16,
        'axes.labelsize': 16,
        'axes.titlesize': 16,
        'savefig.dpi': 600,
        'figure.dpi': 600
    })
    
    if plot_type == 'donut':
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            df['Percentage'],
            wedgeprops={'width': 0.4, 'edgecolor': 'w', 'linewidth': 0.5},
            colors=[REGION_COLORS[r] for r in df['Region']],
            startangle=90,
            autopct=lambda p: f'{p:.1f}',
            pctdistance=0.8
        )
        
        centre_circle = plt.Circle((0,0), 0.2, color='white')
        ax.add_artist(centre_circle)
        ax.text(0, 0, f'Total: {total:.1f}\n({subtype})', 
                ha='center', va='center', fontsize=16)
        # no box
        # 2 rows
        ax.legend(wedges, df['Region'],
            title="Regions",
            loc="center left",
            frameon=False,
            # ncol=3,
            bbox_to_anchor=(1, 0.5))
        
    elif plot_type == 'bar':
        fig, ax = plt.subplots(figsize=(8, 1))
        bottom = 0
        for idx, row in df.iterrows():
            ax.barh(0, row['Percentage'], 
                    left=bottom, 
                    color=REGION_COLORS[row['Region']],
                    edgecolor='white')
            if row['Percentage'] > 5:
                ax.text(bottom + row['Percentage'] / 2, 0, 
                        f"{row['Percentage']:.1f}", 
                        ha='center', va='center', 
                        color='black', fontsize=16)
            bottom += row['Percentage']
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        
        ax.set_xlim(0, 100)
        # ax.text(50, -0.3, f'Total Time: {total:.1f} ({subtype})', 
        #         ha='center', va='center', fontsize=12)
        
    else:
        raise ValueError("Invalid plot_type. Choose 'donut' or 'bar'")
    
    plt.tight_layout()
    plt.savefig(f'virus_data_{subtype}_{plot_type}.png', bbox_inches='tight')
    plt.savefig(f'virus_data_{subtype}_{plot_type}.svg', bbox_inches='tight')
    # plt.show()


visualize_virus_data('H7', 'donut') 
visualize_virus_data('H7N3', 'bar') 
visualize_virus_data('H7N7', 'bar') 
visualize_virus_data('H7N9', 'bar')

visualize_virus_data('H7N9', 'donut') 