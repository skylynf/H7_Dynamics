#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# ──────────────────────────────────────────
# ──────────────────────────────────────────
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "figure.dpi": 600,
    "savefig.dpi": 600,
    "font.family": "Arial",
})

# ──────────────────────────────────────────
# ──────────────────────────────────────────
world = gpd.read_file(
    "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)
world = world[world.name != "Antarctica"]

nodes = pd.DataFrame(
    {
        "country": ["North America", "Europe", "South America", "Asia", "Africa", "Oceania"],
        "long": [-100, 0, -60, 90, 30, 140],
        "lat": [40, 50, -20, 30, 20, -30],
    }
)

# ──────────────────────────────────────────
# ──────────────────────────────────────────

subtype_name = "H7N9"
show_legend = False

df = pd.read_excel("H7_map(1).xlsx", sheet_name=subtype_name)
df.columns = df.columns.str.strip()

df = (
    df.merge(nodes, left_on="From", right_on="country", how="left")
      .merge(nodes, left_on="To", right_on="country", suffixes=("_start", "_end"), how="left")
)

print(f"Total migrations: {len(df)}")
print("Migrations data:\n", df.head())

# ──────────────────────────────────────────
# ──────────────────────────────────────────
def bf_to_color(bf: float) -> str:
    if bf > 5000:
        return "#C90000"
    if bf > 500:
        return "#FF5100"
    if bf > 50:
        return "#FF8800"
    if bf > 5:
        return "#FFBB00"
    return "#9E9E9E"

def jump_to_width(jump: float) -> float:
    return 4 if jump > 5 else 1 + 0.5 * jump

def pp_to_linestyle(pp: float) -> str | None:
    if pp > 0.9:
        return "-"
    if pp > 0.3:
        return "--"
    if pp > 0.1:
        return ":"
    return None

# ──────────────────────────────────────────
# ──────────────────────────────────────────
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor="#F0F0F0")
ax.add_feature(cfeature.OCEAN, facecolor="#D1E5F0")
ax.add_feature(cfeature.COASTLINE, edgecolor="black", linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

ax.set_global()
ax.set_extent([-180, 180, -60, 80], crs=ccrs.PlateCarree())

ax.scatter(
    nodes["long"],
    nodes["lat"],
    s=80,
    c="#2D2D2D",
    edgecolor="white",
    linewidth=1,
    zorder=5,
    transform=ccrs.PlateCarree(),
)

for _, r in nodes.iterrows():
    ax.text(
        r["long"] + 3,
        r["lat"] + 3,
        r["country"],
        fontsize=10,
        weight="bold",
        ha="left",
        va="center",
        transform=ccrs.PlateCarree(),
        zorder=6,
    )

# ──────────────────────────────────────────
# ──────────────────────────────────────────
for _, r in df.iterrows():
    linestyle = pp_to_linestyle(r["PP"])
    if linestyle is None:
        continue

    color = bf_to_color(r["BF"])
    width = jump_to_width(r["MJ"])

    ax.annotate(
        "",
        xy=(r["long_end"], r["lat_end"]),
        xytext=(r["long_start"], r["lat_start"]),
        arrowprops=dict(
            arrowstyle="-|>",
            connectionstyle="arc3,rad=0.2",
            color=color,
            linewidth=width,
            linestyle=linestyle,
            shrinkA=6,
            shrinkB=6,
        ),
        transform=ccrs.PlateCarree(),
        zorder=4,
    )

# ──────────────────────────────────────────
# ──────────────────────────────────────────
color_handles = [
    Line2D([0], [0], color="#C90000", lw=2, label="BF > 5000"),
    Line2D([0], [0], color="#FF5100", lw=2, label="BF > 500"),
    Line2D([0], [0], color="#FF8800", lw=2, label="BF > 50"),
    Line2D([0], [0], color="#FFBB00", lw=2, label="BF > 5"),
    Line2D([0], [0], color="#9E9E9E", lw=2, label="BF ≤ 5"),
]

width_handles = [
    Line2D([0], [0], color="black", lw=4, label="MJ > 5"),
    # Line2D([0], [0], color="black", lw=3.5, label="MJ = 5"),
    Line2D([0], [0], color="black", lw=2.5, label="MJ > 3"),
    Line2D([0], [0], color="black", lw=2, label="MJ > 1"),
]

style_handles = [
    Line2D([0], [0], color="black", lw=2, linestyle="-", label="PP > 0.9"),
    Line2D([0], [0], color="black", lw=2, linestyle="--", label="PP > 0.3"),
    Line2D([0], [0], color="black", lw=2, linestyle=":", label="PP > 0.1"),
]

if show_legend:
    first_legend = ax.legend(
        handles=color_handles,
        title="Bayes factor",
        loc="lower left",
        frameon=False,
        fontsize=10,
        title_fontsize=12,
        bbox_to_anchor=(0.14, 0.01),
    )
    third_legend = ax.legend(
        handles=style_handles,
        title="Posterior",
        loc="lower left",
        frameon=False,
        fontsize=10,
        title_fontsize=12,
        bbox_to_anchor=(0.01, 0.01),
    )
    second_legend = ax.legend(
        handles=width_handles,
        title="Markov Jump",
        loc="lower left",
        frameon=False,
        fontsize=10,
        title_fontsize=12,
        bbox_to_anchor=(0.01, 0.25),
    )

    ax.add_artist(first_legend)
    ax.add_artist(third_legend)

# delete all axes spines
for spine in ax.spines.values():
    spine.set_visible(False)


plt.savefig("Global_Spread_Network_"+ subtype_name + ".png", bbox_inches="tight", pad_inches=0.5)
# save svg
plt.savefig("Global_Spread_Network_"+ subtype_name + ".svg", bbox_inches="tight", pad_inches=0.5)