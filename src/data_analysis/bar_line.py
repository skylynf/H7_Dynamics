#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure 1A – Monthly H7 events (linear-scaled bar, per region) 
                  + yearly WAHIS impact (twin right axis, compact ticks)
作者：<your name>      日期：<yyyy-mm-dd>
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# ──────────────────────────────────────────────────────────────────────────────
sns.set_theme(context="paper", style="ticks", font="Arial", font_scale=1.7)
plt.rcParams.update({
    "axes.linewidth"     : 2,
    'xtick.major.width': 2,
    'ytick.major.width': 2,
    "axes.labelweight"   : "bold",
    "axes.titleweight"   : "bold",
    "legend.frameon"     : False,
    "pdf.fonttype"       : 42,
    "ps.fonttype"        : 42,
    'savefig.dpi': 600,
})

# ──────────────────────────────────────────────────────────────────────────────
h7 = pd.read_csv("H7FAO.csv", encoding="latin1", dtype={"year": str})
regions = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]

h7 = h7[(h7["year"].notna()) & (h7["month"].notna())].copy()
h7["year"]  = h7["year"].astype(int)
h7["month"] = h7["month"].astype(int)
h7 = h7[h7["Region"].isin(regions)][["Region", "year", "month"]]

years  = sorted(h7["year"].unique())
months = range(1, 13)

full_index  = pd.MultiIndex.from_product([regions, years, months],
                                         names=["Region", "year", "month"])
agg_bar     = (h7.groupby(["Region", "year", "month"])
                   .size()
                   .reindex(full_index, fill_value=0)
                   .rename("freq")
                   .reset_index())
agg_bar["year_code"] = pd.Categorical(agg_bar["year"], categories=years).codes

# ──────────────────────────────────────────────────────────────────────────────

wahis = pd.read_csv("epanAfricaqinliuganWAHIS.csv", encoding="latin1", dtype={"Year": str})
wahis["Year"] = wahis["Year"].astype(int)
agg_line = (wahis.groupby("Year")
            .agg(Total_Cases     =("Cases",       "sum"),
                 Total_Killed     =("Killed",      "sum"),
                 Total_Slaughter  =("Slaughtered", "sum"),
                 Total_Deaths     =("Deaths",      "sum"))
            .reset_index()
            .rename(columns={"Year": "year"}))
agg_line["year_code"] = pd.Categorical(agg_line["year"], categories=years).codes

left_max  = max(1, agg_bar["freq"].max())
right_max = agg_line.iloc[:, 1:5].to_numpy().max()
scale_fac = left_max / right_max

for col in ["Total_Cases", "Total_Killed", "Total_Slaughter", "Total_Deaths"]:
    agg_line[f"{col}_scaled"] = agg_line[col] * scale_fac

# ──────────────────────────────────────────────────────────────────────────────




fig, ax1 = plt.subplots(figsize=(13, 7))
ax2 = ax1.twinx()
ax2.spines["right"].set_visible(True)

cluster_w  = 0.8
n_regions  = len(regions)
bar_w      = cluster_w / n_regions
bar_bottom_offset = 0.1

region_fill = {                        
    "Africa"        : "#1f78b4",
    "Asia"          : "#e31a1c",
    "Europe"        : "#b2df8a",
    "North America" : "#33a02c",
    "Oceania"       : "#ff7f00",
    "South America" : "#a6cee3",
}

for r_idx, region in enumerate(regions):
    for m_idx, month in enumerate(months):
        sub = agg_bar[(agg_bar["Region"] == region) & (agg_bar["month"] == month)]
        x_base = sub["year_code"] + (month - 6.5) / 12
        x_pos  = x_base - cluster_w/2 + (r_idx + 0.5) * bar_w

        ax1.bar(
            x_pos,
            sub["freq"].replace(0, np.nan),
            width      = bar_w,
            bottom     = bar_bottom_offset,
            color      = region_fill[region],
            edgecolor  = "black",
            linewidth  = 1.0,
            label      = region if month == 1 else "_nolegend_"
        )

line_offset = 0.5

line_style_map = {
    "Total_Cases_scaled"     : ("o", "-",  "black"),
    "Total_Slaughter_scaled" : ("s", "--", "black"),
    "Total_Killed_scaled"    : ("D", "-.", "black"),
    "Total_Deaths_scaled"    : ("^", ":",  "black")
}

for col, (marker, lstyle, color) in line_style_map.items():
    ax2.plot(
        agg_line["year_code"],
        agg_line[col] + line_offset,
        marker     = marker,
        markersize = 5,
        linewidth  = 1.8,
        linestyle  = lstyle,
        color      = color,
        label      = col.replace("_scaled", "").replace("Total_", "").replace("_", " ")
    )

# ──────────────────────────────────────────────────────────────────────────────
ax1.set_ylim()  # Modified from bar_bottom_offset to 0
ax1.set_ylabel("")  
ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

ax1.set_xlim(agg_bar["year_code"].min() - 4, agg_bar["year_code"].max() + 1)
# ax1.set_xlabel("Year", fontweight="bold")
ax1.set_xticks(range(len(years))[::2])  
ax1.set_xticklabels(years[::2])         

def human_fmt(x, pos):
    if x == 0: return "0"
    x = x / scale_fac
    for unit in ["", "k", "M", "B"]:
        if abs(x) < 1000:
            return f"{x:,.0f}{unit}"
        x /= 1000
    return f"{x:.1f}T"
ax2.yaxis.set_major_formatter(FuncFormatter(human_fmt))
ax2.set_ylim()
ax2.set_ylabel("")  

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

leg1 = ax1.legend(handles1, labels1,
                  title="Region",
                  loc="upper left",
                  bbox_to_anchor=(0.02, 1.00),
                  frameon=False)
leg2 = ax2.legend(handles2, labels2,
                  title="WAHIS Variable",
                  loc="upper left",
                  bbox_to_anchor=(0.02, 0.5),
                  frameon=False)

sns.despine(ax=ax1, top=True, right=True)  
ax2.spines["top"].set_visible(False)      
ax2.spines["left"].set_visible(False)     
fig.tight_layout(pad=1.2)

fig.savefig("H7_domestic_bar_line.svg", bbox_inches="tight", dpi=600)

plt.show()