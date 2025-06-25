#!/usr/bin/env python3
"""
Create publication-ready violin plots for GLM coefficients from BEAST .log file.
"""

import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arviz as az

# Set professional plotting parameters
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "figure.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
    "pdf.fonttype": 42
})

# User settings
LOG_PATH = pathlib.Path("H7glm.country.glm.log")
BURN_IN_FRAC = 0.10
OUTFILE = "GLM_coefficients_violin.pdf"

# Predictor names mapping
PREDICTOR_NAMES = {
    1: "Population Density",
    2: "Urbanization",
    3: "GDP per Capita",
    4: "Healthcare Access",
    5: "Temperature",
    6: "Precipitation",
    7: "Border Traffic",
    8: "Travel Volume",
    9: "Vaccination Rate",
    10: "Public Awareness",
    11: "Early Detection",
    12: "Policy Response",
    13: "Seasonality",
    14: "Animal Reservoir",
    15: "Genetic Diversity"
}

def main():
    print("Processing BEAST log file...")
    
    # Read and clean data
    df = pd.read_csv(LOG_PATH, sep=r"\s+", comment="#")
    burn_in_n = int(len(df) * BURN_IN_FRAC)
    df_posterior = df.iloc[burn_in_n:].reset_index(drop=True)
    
    # Extract coefficients
    coef_cols = [c for c in df_posterior.columns 
                 if c.startswith("country.coefficientsTimesIndicators")]
    df_coef = df_posterior[coef_cols].copy()
    
    # Prepare data for plotting
    long_df = df_coef.melt(var_name="predictor", value_name="coefficient")
    long_df["predictor_idx"] = long_df["predictor"].str.extract(r"(\d+)$").astype(int)
    long_df["predictor_name"] = long_df["predictor_idx"].map(PREDICTOR_NAMES)
    
    # Calculate statistics for ordering
    stats = long_df.groupby("predictor_name")["coefficient"].agg(
        mean_effect="mean",
        abs_effect=lambda x: np.abs(x).mean(),
        inclusion_prob=lambda x: (x != 0).mean()
    ).reset_index()
    
    # Order predictors by absolute effect size
    stats = stats.sort_values("abs_effect", ascending=False)
    predictor_order = stats["predictor_name"].tolist()
    
    print("Creating violin plot...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create violin plot
    sns.violinplot(
        data=long_df,
        x="predictor_name",
        y="coefficient",
        order=predictor_order,
        palette="viridis",
        cut=0,
        inner="box",
        linewidth=0.8,
        saturation=0.8,
        ax=ax
    )
    
    # Add horizontal line at zero
    ax.axhline(0, color="grey", linestyle="--", linewidth=0.8, alpha=0.7)
    
    # Customize appearance
    ax.set_xlabel("Predictor Variables", fontweight="medium", labelpad=10)
    ax.set_ylabel("Coefficient Estimate", fontweight="medium", labelpad=8)
    ax.set_title("Posterior Distributions of GLM Coefficients", pad=12)
    
    # Rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add grid for readability
    ax.grid(True, axis="y", linestyle="--", alpha=0.3)
    
    # Add data points to show density
    sns.stripplot(
        data=long_df,
        x="predictor_name",
        y="coefficient",
        order=predictor_order,
        color="black",
        alpha=0.15,
        size=1.5,
        jitter=0.2,
        ax=ax
    )
    
    # Add inclusion probability to each plot
    for i, pred in enumerate(predictor_order):
        prob = stats.loc[stats["predictor_name"] == pred, "inclusion_prob"].values[0]
        ax.text(
            i, ax.get_ylim()[0] + 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
            f"{prob:.0%}",
            ha="center",
            va="bottom",
            fontsize=7,
            bbox=dict(facecolor="white", alpha=0.7, pad=1, edgecolor="none")
        )
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color="blue", lw=2, label='Coefficient Distribution'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
               markersize=4, label='Individual Samples'),
        Line2D([0], [0], color='grey', linestyle='--', lw=1, label='Zero Reference')
    ]
    ax.legend(handles=legend_elements, loc="best", frameon=True, framealpha=0.8)
    
    # Add explanatory text
    fig.text(
        0.5, 0.01,
        "Numbers below each violin show the posterior inclusion probability. "
        "Violins show kernel density estimates of posterior distributions.",
        ha="center",
        fontsize=8,
        color="#555555"
    )
    
    # Save figure
    plt.tight_layout()
    fig.savefig(OUTFILE)
    print(f"Successfully created violin plot: {OUTFILE}")

if __name__ == "__main__":
    main()