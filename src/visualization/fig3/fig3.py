import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import colormaps
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'font.family': 'Arial'
})

world = gpd.read_file(
    "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)
world = world[world.name != "Antarctica"]

nodes = pd.DataFrame({
    'country': ["NorthAmerica", "EU", "SA", "Asia", "AF", "Oceania"],
    'long': [-100, 0, -60, 90, 30, 140],
    'lat': [40, 50, -20, 30, 20, -30]
})

path_data = pd.DataFrame({
    'from': ['NorthAmerica', 'EU', 'Asia', 'AF', 'Oceania'],
    'to': ['EU', 'Asia', 'AF', 'Oceania', 'NorthAmerica'],
    'markov_jump_group': ['0-1', '1-5', '>5', '1-5', '0-1']
})

path = path_data.merge(nodes, left_on='from', right_on='country') \
               .merge(nodes, left_on='to', right_on='country', suffixes=('_start', '_end'))

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor='#F0F0F0')
ax.add_feature(cfeature.OCEAN, facecolor='#D1E5F0')
ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

ax.set_global()
ax.set_extent([-180, 180, -60, 80], crs=ccrs.PlateCarree())

ax.scatter(nodes['long'], nodes['lat'], s=80, c='#2D2D2D', 
          edgecolor='white', linewidth=1, zorder=5, 
          transform=ccrs.PlateCarree())

for idx, row in nodes.iterrows():
    ax.text(row['long']+3, row['lat']+3, row['country'],
           fontsize=10, weight='bold', ha='left', va='center',
           transform=ccrs.PlateCarree())

color_mapping = {'0-1': '#808080', '1-5': '#FFA500', '>5': '#FF0000'}
width_mapping = {'0-1': 1.0, '1-5': 2.0, '>5': 3.0}

for _, row in path.iterrows():
    control_point = (
        (row['long_start'] + row['long_end']) / 2 + np.random.uniform(-10, 10),
        (row['lat_start'] + row['lat_end']) / 2 + np.random.uniform(-5, 5)
    )
    
    arrow = ax.annotate('',
        xy=(row['long_end'], row['lat_end']),
        xytext=(row['long_start'], row['lat_start']),
        arrowprops=dict(
            arrowstyle='fancy',
            connectionstyle=f"arc3,rad=0.2",
            color=color_mapping[row['markov_jump_group']],
            linewidth=width_mapping[row['markov_jump_group']],
            shrinkA=7,
            shrinkB=7
        ),
        transform=ccrs.PlateCarree()
    )

legend_elements = [
    plt.Line2D([0], [0], color='#808080', lw=2, label='0-1 Jumps'),
    plt.Line2D([0], [0], color='#FFA500', lw=2, label='1-5 Jumps'),
    plt.Line2D([0], [0], color='#FF0000', lw=2, label='>5 Jumps')
]

ax.legend(handles=legend_elements, 
         loc='lower left',
         frameon=True,
         title='Markov Jump Groups',
         title_fontsize=12)

# ax.add_artist(ScaleBar(ax))
# ax.add_artist(NorthArrow(ax))

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

plt.title('Global Spread Network of Avian Influenza H7N3\nBayesian Markov Jump Analysis', 
         fontsize=16, pad=20)

plt.savefig('Global_Spread_Network.png', 
           bbox_inches='tight', 
           pad_inches=0.5,
           dpi=600)
plt.show()