from pathlib import Path
import sys
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_cleaned_dataset(dataset_path: Path) -> pd.DataFrame:
    """Load the cleaned churn dataset from a CSV file."""
    try:
        df = pd.read_csv(dataset_path)
        print(f"Loaded cleaned dataset: {dataset_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Cleaned dataset not found: {dataset_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Cleaned dataset is empty: {dataset_path}")
    except Exception as error:
        raise RuntimeError(f"Failed to load cleaned dataset: {error}") from error


def ensure_images_folder(images_path: Path) -> None:
    """Create the images folder if it does not already exist."""
    try:
        images_path.mkdir(parents=True, exist_ok=True)
        print(f"Image folder ready: {images_path}")
    except Exception as error:
        raise RuntimeError(f"Unable to create images folder: {error}") from error


def save_figure(fig: plt.Figure, filepath: Path) -> None:
    """Save the matplotlib figure as a PNG and close it."""
    try:
        fig.tight_layout()
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        print(f"Saved chart: {filepath}")
    except Exception as error:
        raise RuntimeError(f"Failed to save figure {filepath}: {error}") from error


def print_insights(title: str, insights: List[str]) -> None:
    """Print business insights for a visualization."""
    print(f"\nInsights for {title}:")
    for insight in insights:
        print(f"- {insight}")


def plot_churn_distribution(df: pd.DataFrame, images_path: Path) -> None:
    """Plot churn distribution as a count plot."""
    churn_counts = df["Churn"].value_counts().reindex(["No", "Yes"]).fillna(0)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=churn_counts.index, y=churn_counts.values, palette=["#4CAF50", "#F44336"], ax=ax)
    ax.set_title("Churn Distribution")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Number of Customers")
    save_figure(fig, images_path / "churn_distribution.png")

    churn_rate = churn_counts["Yes"] / churn_counts.sum() * 100
    print_insights(
        "Churn Distribution",
        [
            f"Total churn rate is {churn_rate:.1f}% of customers.",
            "A majority of customers are retained, but the churn base is still substantial.",
            "Reducing churn by a few percentage points could materially improve annual revenue." 
        ],
    )


def plot_category_churn(df: pd.DataFrame, category: str, images_path: Path) -> None:
    """Plot churn rate for a categorical variable."""
    cross = pd.crosstab(df[category], df["Churn"], normalize="index") * 100
    cross = cross.reindex(index=cross.index.sort_values())
    fig, ax = plt.subplots(figsize=(10, 6))
    cross.plot(kind="bar", stacked=True, ax=ax, color=["#4CAF50", "#F44336"])
    ax.set_title(f"{category} vs Churn")
    ax.set_xlabel(category)
    ax.set_ylabel("Percentage of Customers")
    ax.legend(title="Churn")
    save_figure(fig, images_path / f"{category.lower().replace(' ', '_')}_vs_churn.png")

    churn_rate_by_category = (cross["Yes"]).sort_values(ascending=False)
    highest = churn_rate_by_category.index[0]
    highest_rate = churn_rate_by_category.iloc[0]
    insights = [
        f"{highest} has the highest churn rate at {highest_rate:.1f}%.",
        f"Churn rates vary significantly across {category.lower()} categories.",
    ]
    if len(churn_rate_by_category) > 1:
        lowest = churn_rate_by_category.index[-1]
        lowest_rate = churn_rate_by_category.iloc[-1]
        insights.append(f"{lowest} has the lowest churn rate at {lowest_rate:.1f}%.")

    print_insights(f"{category} vs Churn", insights)


def plot_numeric_distribution(df: pd.DataFrame, column: str, images_path: Path) -> None:
    """Plot a numeric feature distribution with a KDE overlay."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[column], kde=True, bins=30, color="#1976D2", ax=ax)
    ax.set_title(f"{column} Distribution")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    save_figure(fig, images_path / f"{column.lower().replace(' ', '_')}_distribution.png")

    mean_value = df[column].mean()
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    print_insights(
        f"{column} Distribution",
        [
            f"Average {column.lower()} is {mean_value:.2f}.",
            f"The middle 50% of values ranges from {q1:.2f} to {q3:.2f}.",
        ],
    )


def plot_monthly_charges_by_churn(df: pd.DataFrame, images_path: Path) -> None:
    """Plot Monthly Charges grouped by churn status using a boxplot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="Churn", y="MonthlyCharges", data=df, palette=["#4CAF50", "#F44336"], ax=ax)
    ax.set_title("Monthly Charges by Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Monthly Charges")
    save_figure(fig, images_path / "monthly_charges_by_churn_boxplot.png")

    mean_churn = df.groupby("Churn")["MonthlyCharges"].mean()
    print_insights(
        "Monthly Charges by Churn",
        [
            f"Customers who churn tend to have higher average monthly charges ({mean_churn['Yes']:.2f}) than retained customers ({mean_churn['No']:.2f}).",
            "Pricing pressure is likely a key factor for churn and should be evaluated for at-risk segments.",
        ],
    )


def plot_tenure_vs_monthly_charges(df: pd.DataFrame, images_path: Path) -> None:
    """Plot tenure against monthly charges using a scatter plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x="tenure", y="MonthlyCharges", hue="Churn", data=df, palette={"No": "#4CAF50", "Yes": "#F44336"}, alpha=0.7, ax=ax)
    ax.set_title("Tenure vs Monthly Charges")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Monthly Charges")
    ax.legend(title="Churn")
    save_figure(fig, images_path / "tenure_vs_monthly_charges_scatter.png")

    correlation = df["tenure"].corr(df["MonthlyCharges"])
    print_insights(
        "Tenure vs Monthly Charges",
        [
            f"The correlation between tenure and monthly charges is {correlation:.2f}.",
            "Customers with short tenure and high monthly charges are an important churn risk group.",
        ],
    )


def plot_correlation_heatmap(df: pd.DataFrame, images_path: Path) -> None:
    """Plot a correlation heatmap for numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Heatmap for Numerical Columns")
    save_figure(fig, images_path / "correlation_heatmap.png")

    strongest = correlation_matrix.unstack().sort_values(ascending=False)
    strongest = strongest[strongest < 1.0]
    top_pair = strongest.idxmax()
    print_insights(
        "Correlation Heatmap",
        [
            f"Strongest positive numeric correlation is between {top_pair[0]} and {top_pair[1]} ({strongest.max():.2f}).",
            "Correlation analysis helps prioritize features for customer retention modeling.",
        ],
    )


def calculate_summary_metrics(df: pd.DataFrame) -> Tuple[int, float, float, float, float, float]:
    """Calculate summary business metrics from the dataset."""
    total_customers = len(df)
    churn_rate = df["Churn"].eq("Yes").mean() * 100
    retention_rate = df["Churn"].eq("No").mean() * 100
    average_monthly = df["MonthlyCharges"].mean()
    average_tenure = df["tenure"].mean()
    revenue_lost = df.loc[df["Churn"] == "Yes", "MonthlyCharges"].sum() * 12
    return total_customers, churn_rate, retention_rate, average_monthly, average_tenure, revenue_lost


def generate_business_insights(df: pd.DataFrame) -> List[str]:
    """Generate a list of top business insights based on churn patterns."""
    churn_rate = df["Churn"].eq("Yes").mean() * 100
    contract_churn = pd.crosstab(df["Contract"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    internet_churn = pd.crosstab(df["InternetService"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    payment_churn = pd.crosstab(df["PaymentMethod"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    senior_churn = pd.crosstab(df["SeniorCitizen"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    high_risk_contract = contract_churn.index[0]
    high_risk_internet = internet_churn.index[0]
    high_risk_payment = payment_churn.index[0]
    high_risk_senior = senior_churn.index[0]

    return [
        f"Overall churn rate is {churn_rate:.1f}%.",
        f"Month-to-month customers are the highest churn risk, especially compared to longer-term contracts.",
        f"Customers with {high_risk_internet} internet service have the largest churn rate among internet types.",
        f"Payment by {high_risk_payment} shows the highest proportion of churned customers.",
        f"{high_risk_senior} customers have a higher relative churn rate than their counterparts.",
    ]


def generate_business_recommendations(df: pd.DataFrame) -> List[str]:
    """Generate a list of business recommendations using churn analysis."""
    contract_churn = pd.crosstab(df["Contract"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    internet_churn = pd.crosstab(df["InternetService"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    payment_churn = pd.crosstab(df["PaymentMethod"], df["Churn"], normalize="index")["Yes"].sort_values(ascending=False)
    top_contract = contract_churn.index[0]
    top_internet = internet_churn.index[0]
    top_payment = payment_churn.index[0]

    return [
        f"Create targeted retention offers for {top_contract} customers to reduce churn from the high-risk segment.",
        f"Review pricing, support, and service quality for {top_internet} internet customers to improve loyalty.",
        f"Simplify or incentivize lower-churn payment methods to move customers away from {top_payment}.",
        "Use monthly charge sensitivity when designing promotions, since higher-priced accounts churn more often.",
        "Prioritize early-tenure customers with proactive onboarding and value reinforcement programs.",
    ]


def print_summary(df: pd.DataFrame) -> None:
    """Print aggregated business metrics and insights."""
    metrics = calculate_summary_metrics(df)
    insights = generate_business_insights(df)
    recommendations = generate_business_recommendations(df)

    print("\nSummary Metrics:")
    print(f"- Total Customers: {metrics[0]}")
    print(f"- Churn Rate: {metrics[1]:.1f}%")
    print(f"- Retention Rate: {metrics[2]:.1f}%")
    print(f"- Average Monthly Charges: ${metrics[3]:.2f}")
    print(f"- Average Tenure: {metrics[4]:.1f} months")
    print(f"- Estimated Annual Revenue Lost due to Churn: ${metrics[5]:,.2f}")

    print("\nTop 5 Business Insights:")
    for insight in insights:
        print(f"- {insight}")

    print("\nTop 5 Business Recommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")


def main() -> None:
    """Main entry point for exploratory data analysis."""
    root_path = Path(__file__).resolve().parent.parent
    dataset_path = root_path / "data" / "cleaned_churn.csv"
    images_path = root_path / "images"

    try:
        df = load_cleaned_dataset(dataset_path)
        ensure_images_folder(images_path)

        sns.set_theme(style="whitegrid")

        plot_churn_distribution(df, images_path)
        plot_category_churn(df, "gender", images_path)
        plot_category_churn(df, "SeniorCitizen", images_path)
        plot_category_churn(df, "Contract", images_path)
        plot_category_churn(df, "InternetService", images_path)
        plot_category_churn(df, "PaymentMethod", images_path)
        plot_numeric_distribution(df, "MonthlyCharges", images_path)
        plot_numeric_distribution(df, "tenure", images_path)
        plot_monthly_charges_by_churn(df, images_path)
        plot_tenure_vs_monthly_charges(df, images_path)
        plot_correlation_heatmap(df, images_path)

        print_summary(df)
    except Exception as error:
        print(f"Error during exploratory data analysis: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
