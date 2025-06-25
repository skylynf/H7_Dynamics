## Project Overview
This repository contains the full analysis pipeline and figure-generating scripts for the manuscript *Global transmission dynamics of avian influenza H7 subtypes* (submitted to *Nature Communications*).

The code base includes:
- Bayesian phylogeographic analyses (continuous, discrete, GLM)
- Host-specific diffusion analyses
- Wavefront diffusion calculations
- End-to-end Python / R scripts to reproduce all main-text and supplementary figures

All analyses were developed and tested with **Python ≥ 3.9** and **R ≥ 4.2** on Windows 10, macOS 12, and Ubuntu 20.04.

---

## Software Requirements

### External Software
- BioAider v1.5.2
- MAFFT v7.526
- AliView v1.28
- trimAL v1.4
- IQ-TREE v2.0.7
- TreeTime v0.11.3
- BEAST v1.10.4
- Tracer v1.7.2
- TreeAnnotator v1.10.4
- FigTree v1.4.4
- SpreadD3 v0.9.7

### R Packages
- seraphim
- diagram
- devtools
- raster
- rnaturalearth
- rnaturalearthdata

### Python Packages
See `requirements.txt` for a full list. Key dependencies include:
- pandas, numpy, matplotlib, seaborn
- geopandas, cartopy, shapely, openpyxl

---

## Repository Layout
```
data/                  # Raw input data (FAO, OIE, human cases, etc.)
output/                # Example result files (XML, MCC trees, coefficient tables)
src/
  continuous/          # Continuous diffusion BEAST XML + R visualisation scripts
  discrete/            # Discrete diffusion BEAST XML files
  glm/                 # GLM input tables and visualisation scripts
  host/                # Host-specific diffusion analyses
  wavefront_diffusion/ # Wavefront distance & diffusion-coefficient analyses
  visualization/       # Publication-quality figure scripts (Python / R)
  data_analysis/       # Auxiliary data analysis scripts
  deprecated/          # Obsolete or exploratory scripts kept for reference
```

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-org>/h7-transmission.git
cd h7-transmission
```

### 2. Install Python dependencies
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install R and required R packages
Launch an R session and run:
```r
install.packages(c(
  "seraphim", "diagram", "devtools", "raster", "rnaturalearth", "rnaturalearthdata"
))
# If seraphim is not available on CRAN, install from GitHub:
if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
remotes::install_github("phylogeography/seraphim")
```

### 4. Install external software
Please download and install the following software (links provided):
- [BioAider v1.5.2](https://github.com/bioaider/BioAider)
- [MAFFT v7.526](https://mafft.cbrc.jp/alignment/software/)
- [AliView v1.28](https://ormbunkar.se/aliview/)
- [trimAL v1.4](http://trimal.cgenomics.org/)
- [IQ-TREE v2.0.7](http://www.iqtree.org/)
- [TreeTime v0.11.3](https://github.com/neherlab/treetime)
- [BEAST v1.10.4](https://beast.community/)
- [Tracer v1.7.2](https://beast.community/tracer)
- [TreeAnnotator v1.10.4](https://beast.community/treeannotator)
- [FigTree v1.4.4](https://github.com/rambaut/figtree/releases)
- [SpreadD3 v0.9.7](https://rega.kuleuven.be/cev/ecv/software/spreadd3)

---

## Example Data and Expected Output
- Example input data are provided in the `data/` directory (e.g., FAO, OIE, human case files).
- Example output files (XML, MCC trees, coefficient tables) are provided in the `output/` directory.
- Each analysis script in `src/` is annotated with required input files and expected output files in the header comments or a local README.
- To reproduce a figure (e.g., Figure 3):
  ```bash
  cd src/visualization/fig3
  python fig3.py
  # or: Rscript fig3chart.R
  ```
  Output graphics will be written to the same folder.

---

## Running the Full Pipeline
1. Prepare all required input data in the `data/` directory.
2. Follow the instructions in each `src/` subdirectory README or script header to run the relevant analysis (Python or R).
3. Use the provided example data and scripts to verify that your environment is set up correctly. Expected output files are provided in `output/` for comparison.

---

## License
The code is released under the MIT License (see `LICENSE`). Data files are distributed for academic use only; please consult the original sources for licensing details.
