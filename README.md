# Customer Churn Analytics & Business Intelligence Dashboard

## Project Overview
This project analyzes the IBM Telco Customer Churn dataset to identify drivers of customer churn, calculate business KPIs, and produce visualizations and SQL reports suitable for a BI dashboard. It provides data preprocessing, exploratory data analysis (EDA), and SQL-based analysis to support retention strategies.

## Business Problem
Customer churn reduces recurring revenue and increases acquisition costs. The goal is to quantify churn, identify at-risk customer segments, estimate revenue impact, and recommend data-driven actions to reduce churn and increase lifetime value.

## Objectives
- Clean and prepare the Telco churn dataset.
- Produce a set of high-quality visualizations highlighting churn drivers.
- Calculate business KPIs and estimated revenue at risk.
- Provide SQL queries for reporting and dashboarding.
- Deliver actionable business insights and recommendations.

## Dataset Description
The dataset `WA_Fn-UseC_-Telco-Customer-Churn.csv` contains customer-level records with columns such as:
- `customerID`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `tenure`
- `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`
- `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`
- `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`, `Churn`

Place the raw CSV in the `data/` folder. The cleaned dataset is saved as `data/cleaned_churn.csv` by the preprocessing script.

## Technology Stack
- Python 3.12
- pandas, numpy
- matplotlib, seaborn
- SQL (PostgreSQL / MySQL compatible)

## Project Structure
- `data/` — Raw and processed datasets
- `src/` — Python modules: `data_preprocessing.py`, `eda.py`
- `sql/` — Analysis SQL script `analysis.sql` and views
- `images/` — Output visualizations (PNG)
- `notebooks/` — Jupyter notebooks for interactive exploration
- `dashboard/` — (Optional) BI assets or dashboard templates

## Data Cleaning Steps
Implemented in `src/data_preprocessing.py`:
- Load CSV and print dataset info.
- Replace blank `TotalCharges` values with `NaN` and coerce to numeric.
- Impute or fill `TotalCharges` using `MonthlyCharges * tenure` or 0 where appropriate.
- Convert `SeniorCitizen` from `0/1` to `No/Yes`.
- Trim whitespace in string columns and normalize categorical labels.
- Remove duplicate rows and duplicate `customerID` entries.
- Save cleaned output to `data/cleaned_churn.csv`.

## Exploratory Data Analysis
Implemented in `src/eda.py`:
- Generates charts including churn distribution, categorical churn breakdowns, numeric distributions, boxplots, scatterplots, and a correlation heatmap.
- Saves all charts to `images/` as high-resolution PNGs.
- Prints concise business insights after each chart.
- Computes KPIs and prints an executive summary, top insights, and recommendations.

## SQL Analysis
The `sql/analysis.sql` file contains 25+ commented SQL queries that answer business questions such as:
- Total customers, churn rate, retention rate
- Churn and revenue breakdowns by contract, internet service, payment method
- Revenue lost due to churn and per-segment revenue risks
- Top customers by charges
- A `customer_summary` view for dashboarding

The SQL is written for compatibility with PostgreSQL and MySQL.

## KPIs Calculated
- Total Customers
- Active Customers
- Churned Customers
- Churn Rate (%)
- Retention Rate (%)
- Average Monthly Charges
- Average Tenure (months)
- Estimated Monthly Revenue
- Estimated Monthly Revenue Lost due to Churn

## Business Insights (examples)
- Month-to-month customers show the highest churn rates — prioritize retention offers.
- High monthly charges correlate with higher churn — consider pricing or value offers.
- Certain internet services (e.g., Fiber) have elevated churn — investigate service quality.
- Early-tenure customers with higher charges are a priority risk group.
- Payment method and contract type are predictive of churn and useful for targeting.

## Recommendations
- Targeted retention campaigns for month-to-month customers.
- Promotional or pricing reviews for high monthly charge segments.
- Improve onboarding and support for early-tenure customers.
- Encourage lower-churn payment methods via incentives.
- Monitor and remediate service quality for high-churn internet types.

## Future Improvements
- Add feature engineering and predict churn probability with a model.
- Build an automated dashboard (e.g., Power BI, Tableau) using `customer_summary` view.
- A/B test retention offers to quantify lift.
- Incorporate external data (marketing, support tickets) to improve models.

## How to Run the Project
1. Create a Python 3.12 virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
2. Place the raw CSV file in `data/WA_Fn-UseC_-Telco-Customer-Churn.csv`.
3. Run preprocessing:
   ```bash
   python src/data_preprocessing.py
   ```
   This creates `data/cleaned_churn.csv`.
4. Run EDA:
   ```bash
   python src/eda.py
   ```
   Visualizations will be written to `images/` and KPIs printed to the console.
5. Use `sql/analysis.sql` to run queries in your SQL environment (PostgreSQL/MySQL).

---

If you'd like, I can also:
- Run the scripts here and attach generated images.
- Add a small Dockerfile for reproducible execution.
- Convert the SQL queries into parameterized views or stored procedures.

Please tell me what you'd like next.