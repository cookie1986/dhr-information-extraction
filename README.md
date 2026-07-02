# Domestic Homicide Reviews (DHR) - Information Extraction Project

> Work in Progress (06-05-26): this repository has been made public before the project is fully finished. The code, documentation, and structure are still subject to change.

## Overview

This repository contains early-stage work for an ongoing information extraction project, using DHR reports obtained from the Home Office as inputs.

The aim of the project is improve accessibility to DHRs and interpretability of their content. A protocol for this project is being made available and will be linked here.

This repository is currently public for visibility and development purposes.

## Research background

The purpose and planned scope of this project are described in a peer-reviewed research protocol published in *PLOS ONE*. The protocol sets out the research aims, research questions, and intended approach that guide the development of this repository.

Please refer to the published protocol for the full study rationale and research questions:

<details>
<summary>Full citation</summary>
Cook, D., Cook, E.A., Roy, S., Thiara, A., & Selvarajah, R. (2026).
A collaborative approach to applying Natural Language Processing (NLP) to Domestic Homicide Reviews (DHRs): A study protocol.
PLOS ONE.
</details>

## Current Status (as of 6th May 2026)

This project is currently under active development. Some components may be incomplete, experimental, undocumented, or likely to change.

At this stage, the repository may include:

- prototype code
- exploratory scripts
- draft experiments
- partial documentation

## Repository Structure

```
.
├── data/          # Data files or data-processing notes
├── scraper/       # Main source code
├── utils/         # Helper functions
├── scripts/       # Utility or experiment scripts
├── notebooks/     # Exploratory notebooks
├── outputs/       # Summary tables and quality checks
├── tests/         # Tests
├── README.md
├── requirements.txt
└── .gitignore
```

This structure may change as the project develops.

## Installation

Installation instructions are not final yet.

For now, a typical setup may look like:

```bash
git clone dhr-information-extraction
cd dhr-information-extraction
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Please note:** requirements.txt is subject to change, may be missing, or incomplete.

## Usage

Usage instructions are still being developed.

Example commands and scripts will be added here once the codebase is more stable.

## Data

A link to the dataset can be found [here](https://zenodo.org/records/21108268).

## Notes

Because this is a work in progress, please do not treat the current codebase as a stable or final implementation.

## License

This repo is made available under the Creative Commons Attribution 4.0 International License (CC BY 4.0). Users may share and adapt the dataset, including for commercial purposes, provided appropriate attribution is given.

See `LICENSE` for details.

## Contact

For questions or comments, please contact [Darren Cook](darren.cook@citystgeorges.ac.uk).