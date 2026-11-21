
# 🦟 DENGUARD AI
## Urban Dengue Early Warning System

DENGUARD AI is a machine learning-based prototype
designed to predict ward-level dengue case burden
2–4 weeks ahead using historical weather and
urban vulnerability data.

## Problem

Dengue outbreaks create major pressure on
urban healthcare systems in Bangladesh.

Our system analyzes weather history and
ward-level conditions to identify areas
that may face increased dengue risk.

## Main Features

- Ward-level dengue prediction
- Multi-week rainfall lag features
- Random Forest Regression
- Random Forest Risk Classification
- Four risk categories:
  Low, Medium, High, Critical
- Interactive Streamlit dashboard
- Weather analysis and model insights

## Dataset

- Total records: 31,320
- Cities: 5
- Wards: 60
- Data period: 2016–2025
- Frequency: Weekly

The dataset was provided by the hackathon challenge.

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- Plotly
- Matplotlib

## Model Performance

Final chronological test results:

### Regression

- MAE: 2.90
- RMSE: 5.21
- R² Score: 0.77

### Risk Classification

- Accuracy: 75.90%
- Macro F1-score: 0.71
- Critical Recall: 0.81

These results are based on the historical test
period and do not represent live outbreak accuracy.

## Installation

Python and pip are required.

1. Clone the repository:

   git clone YOUR_GITHUB_REPOSITORY_URL

2. Enter the project folder:

   cd DENGUARD-AI

3. Install dependencies:

   pip install -r requirements.txt

4. Run the dashboard:

   streamlit run app.py

The dashboard will open in your browser.

## Project Structure

DENGUARD-AI/
- app.py
- data/
  - dengue_features.csv
- models/
  - dengue_models.joblib
- metrics.json
- requirements.txt
- README.md
- ARCHITECTURE.md

## AI and API Disclosure

AI Assistant:
- ChatGPT (OpenAI): Project planning,
  coding assistance, explanations and debugging support.

External APIs:
- No external weather or LLM API is used
  in the current prototype.

## Limitations

- Uses historical data ending on 29 December 2025.
- Does not provide live 2026 outbreak forecasts.
- Risk thresholds are prototype thresholds,
  not official public health alert levels.
- Predictions should support investigation,
  not replace public health decisions.

## Project Status

Stage 1 Hackathon Prototype.
