#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改后的堆叠柱状图代码
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

sns.set_theme(context="paper", style="ticks", font="Times New Roman", font_scale=1.4)
plt.rcParams.update({
    "axes.linewidth"     : 1.0,
    "axes.labelweight"   : "bold",
    "axes.titleweight"   : "bold",
    "legend.frameon"     : False,
    "pdf.fonttype"       : 42,
    "ps.fonttype"        : 42
})

h7 = pd.read_csv("H7FAO.csv", encoding="latin1", dtype={"year": str})
regions = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]

h7 = h7[(h7["year"].notna()) & (h7["month"].notna())].copy()
h7["year"] = h7["year"].astype(int)
h7["month"] = h7["month"].astype(int)
h7 = h7[h7["Region"].isin(regions)][["Region", "year", "month"]]

years = sorted(h7["year"].unique())
months = range(1, 13)

full_index = pd.MultiIndex.from_product([regions, years, months], names=["Region", "year", "month"])
agg_bar = (h7.groupby(["Region", "year", "month"])
           .size()
           .reindex(full_index, fill_value=0)
           .rename("freq")
           .reset_index())
agg_bar["year_code"] = pd.Categorical(agg_bar["year"], categories=years).codes

wahis = pd.read_csv("epanAfricaqinliuganWAHIS.csv", encoding="latin1", dtype={"Year": str})
wahis["Year"] = wahis["Year"].astype(int)
agg_line = (wahis.groupby("Year")
            .agg(Total_Cases=("Cases", "sum"),
                 Total_Killed=("Killed", "sum"),
                 Total_Slaughter=("Slaughtered", "sum"),
                 Total_Deaths=("Deaths", "sum"))
            .reset_index()
            .rename(columns={"Year": "year"}))
agg_line["year_code"] = pd.Categorical(agg_line["year"], categories=years).codes

left_max = max(1, agg_bar["freq"].max())
right_max = agg_line.iloc[:, 1:5].max().max()
scale_fac = left_max / right_max

for col in ["Total_Cases", "Total_Killed", "Total_Slaughter", "Total_Deaths"]:
    agg_line[f"{col}_scaled"] = agg_line[col] * scale_fac

fig, ax1 = plt.subplots(figsize=(13, 6.5))
ax2 = ax1.twinx()
ax2.spines["right"].set_visible(True)

cluster_w = 0.8

agg_bar_pivot = agg_bar.pivot_table(index=['year_code', 'month'], columns='Region', values='freq', fill_value=0).reset_index()

agg_bar_pivot['x'] = agg_bar_pivot['year_code'] + (agg_bar_pivot['month'] - 6.5)/12

for region in regions:
    agg_bar_pivot[region] = agg_bar_pivot[region].replace(0, np.nan)

agg_bar_pivot.sort_values('x', inplace=True)

region_fill = {
    "Africa": "#a6cee3",
    "Asia": "#1f78b4",
    "Europe": "#b2df8a",
    "North America": "#33a02c",
    "Oceania": "#fb9a99",
    "South America": "#e31a1c"
}

bottoms = np.zeros(len(agg_bar_pivot))
for region in regions:
    values = agg_bar_pivot[region].values
    ax1.bar(agg_bar_pivot['x'], values, bottom=bottoms, width=cluster_w,
            color=region_fill[region], edgecolor='black', linewidth=0.4, label=region)
    bottoms += np.nan_to_num(values, nan=0.0)

line_style_map = {
    "Total_Cases_scaled": ("o", "-", "black"),
    "Total_Slaughter_scaled": ("s", "--", "black"),
    "Total_Killed_scaled": ("D", "-.", "black"),
    "Total_Deaths_scaled": ("^", ":", "black")
}

for col, (marker, lstyle, color) in line_style_map.items():
    ax2.plot(agg_line["year_code"], agg_line[col],
             marker=marker, markersize=5, linewidth=1.8, linestyle=lstyle, color=color,
             label=col.replace("_scaled", "").replace("Total_", "").replace("_", " "))

ax1.set_yscale("log")
ax1.set_ylabel("H7 event count (log scale)", fontweight="bold")
ax1.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
ax1.yaxis.set_minor_formatter(NullFormatter())

ax1.set_xlabel("Year", fontweight="bold")
ax1.set_xticks(range(len(years)))
ax1.set_xticklabels(years)

def human_fmt(x, pos):
    x = x / scale_fac
    for unit in ["", "k", "M", "B"]:
        if abs(x) < 1000:
            return f"{x:,.0f}{unit}"
        x /= 1000
    return f"{x:.1f}T"
ax2.yaxis.set_major_formatter(FuncFormatter(human_fmt))
ax2.set_ylabel("WAHIS totals", fontweight="bold")

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
leg1 = ax1.legend(handles1, labels1, title="Region", loc="upper left", bbox_to_anchor=(1.03, 1.0), frameon=False)
leg2 = ax2.legend(handles2, labels2, title="WAHIS variable", loc="upper left", bbox_to_anchor=(1.03, 0.57), frameon=False)

sns.despine(ax=ax1, right=False)
ax2.spines["left"].set_visible(False)
fig.tight_layout(pad=1.2)
plt.title("Monthly H7 events by region with yearly WAHIS impact", pad=12)

plt.show()