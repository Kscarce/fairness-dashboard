# Procedural Fairness in Healthcare AI

This repository holds the code, data, and analysis notebook for an MSc dissertation
(Newcastle University) evaluating **procedural fairness** in a heart disease prediction
model. The evaluation is based on Leventhal's (1980) procedural justice framework,
adapted for healthcare algorithmic decision-making following the approach of
Jabagi et al. (2025). A public survey (n=325) on perceptions of fairness in healthcare
AI is also analysed alongside the technical assessment.

The model itself is a logistic regression classifier trained on the UCI Heart Disease
dataset, evaluated against six procedural fairness criteria (accuracy, bias suppression,
representativeness, consistency, correctability, ethicality), before and after two
fairness-aware mitigation strategies.

## Repository structure

```
fairness-dashboard/
├── app/
│   └── finaldashboard.py           # Streamlit dashboard presenting the findings
├── data/
│   ├── heart.csv                   # UCI Heart Disease dataset (918 records)
│   └── disssurvey (Responses).xlsx # Public survey responses (n=325)
├── notebooks/
│   └── fairness_pipeline.ipynb     # Model training + fairness evaluation pipeline
├── .streamlit/config.toml          # Dashboard theme configuration
├── .devcontainer/devcontainer.json # Codespaces / dev container setup
├── requirements.txt
└── README.md
```

## Running the notebook (`notebooks/fairness_pipeline.ipynb`)

The notebook loads data with `pd.read_csv('heart.csv')` (an unmodified, relative
path), so `heart.csv` must be available in the **same directory the notebook is run
from**:

- **Locally:** copy or symlink `data/heart.csv` into `notebooks/` before running,
  or launch Jupyter with `notebooks/` as the working directory and place a copy of
  `heart.csv` there.
- **Google Colab:** upload `data/heart.csv` to the Colab session root before running
  the notebook — no path changes are needed.

## Running the dashboard (`app/finaldashboard.py`)

```bash
pip install -r requirements.txt
streamlit run app/finaldashboard.py
```

The dashboard loads survey responses from `../data/disssurvey (Responses).xlsx`
(relative to `app/`), so it must be run from the repository root as shown above.

## File overview

| File | Description |
|---|---|
| `app/finaldashboard.py` | Streamlit app with four tabs (Overview, Fairness Assessment, Survey, Discussion) presenting the model's fairness evaluation and survey results. |
| `data/heart.csv` | UCI Heart Disease dataset (fedesoriano, 2021) — 918 patient records used to train and evaluate the prediction model. |
| `data/disssurvey (Responses).xlsx` | Anonymised public survey responses (n=325) on perceptions of fairness in healthcare AI, collected via Google Forms. |
| `notebooks/fairness_pipeline.ipynb` | Full pipeline: model training, baseline fairness evaluation, and fairness-aware mitigation (ExponentiatedGradient/EqualizedOdds, confidence-based flagging). |
| `.streamlit/config.toml` | Theme settings for the Streamlit dashboard. |
| `.devcontainer/devcontainer.json` | GitHub Codespaces configuration; auto-installs dependencies and launches the dashboard. |
| `requirements.txt` | Python dependencies for both the notebook and the dashboard. |

## Attribution

- Heart Disease dataset: fedesoriano (2021), *Heart Failure Prediction Dataset*, sourced from the UCI Machine Learning Repository.
- Procedural fairness framework: Leventhal, G. S. (1980). *What should be done with equity theory?* In K. J. Gergen, M. S. Greenberg, & R. H. Willis (Eds.), *Social Exchange* (pp. 27–55). Springer.
- Healthcare adaptation of the framework: Jabagi et al. (2025).
- Real-world coronary heart disease prevalence benchmarks: British Heart Foundation (2021).

## Author

Kaylee Scarce, Newcastle University, 2026. Supervised by Dr Vlad González-Zelaya.
