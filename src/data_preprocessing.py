from pathlib import Path
import sys
import pandas as pd
import numpy as np


def load_dataset(csv_path: Path) -> pd.DataFrame:
    """Load the Telco Customer Churn dataset from a CSV file."""
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded data from {csv_path} successfully.")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Dataset file is empty: {csv_path}")
    except Exception as error:
        raise RuntimeError(f"Failed to load dataset: {error}") from error


def display_dataset_info(df: pd.DataFrame) -> None:
    """Display basic dataset shape and column information."""
    print("\nDataset shape:", df.shape)
    print("\nColumn information:")
    df.info()


def check_missing_and_duplicates(df: pd.DataFrame) -> None:
    """Check for missing values and duplicate rows."""
    missing_summary = df.isna().sum()
    print("\nMissing values by column:")
    print(missing_summary[missing_summary > 0] if missing_summary.any() else "No missing values found.")

    duplicate_count = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicate_count}")


def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing TotalCharges values and convert the column to numeric."""
    # Replace blank string entries with NaN before numeric conversion.
    df["TotalCharges"] = df["TotalCharges"].replace(" ", np.nan)

    # Coerce any invalid numeric text to NaN.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    missing_total = df["TotalCharges"].isna()
    missing_count = missing_total.sum()
    print(f"\nTotalCharges missing after conversion: {missing_count}")

    if missing_count > 0:
        # If tenure is zero, TotalCharges should be 0. Otherwise, infer from MonthlyCharges * tenure when possible.
        inferred = df.loc[missing_total, "MonthlyCharges"] * df.loc[missing_total, "tenure"]
        df.loc[missing_total, "TotalCharges"] = inferred.fillna(0)

        still_missing = df["TotalCharges"].isna().sum()
        if still_missing > 0:
            print(f"Imputing remaining {still_missing} TotalCharges values with 0.")
            df["TotalCharges"] = df["TotalCharges"].fillna(0)

    return df


def convert_senior_citizen(df: pd.DataFrame) -> pd.DataFrame:
    """Convert SeniorCitizen from numeric code to Yes/No strings."""
    df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Perform general cleaning on dataset columns."""
    # Normalize string values by stripping whitespace from object columns.
    object_columns = df.select_dtypes(include=["object"]).columns
    for col in object_columns:
        df[col] = df[col].astype(str).str.strip()

    # Ensure contract values and churn labels are clean and consistent.
    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].replace({"Yes": "Yes", "No": "No"})

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows and duplicate customer IDs."""
    if "customerID" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["customerID"])
        after = len(df)
        if before != after:
            print(f"Removed {before - after} duplicate customerID rows.")

    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        df = df.drop_duplicates()
        print(f"Removed {duplicate_rows} duplicate rows.")

    return df


def save_cleaned_dataset(df: pd.DataFrame, csv_path: Path) -> None:
    """Save the cleaned dataset to a CSV file."""
    df.to_csv(csv_path, index=False)
    print(f"Cleaned dataset saved to {csv_path}.")


def main() -> None:
    """Main entry point for the preprocessing script."""
    base_dir = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    output_path = base_dir / "data" / "cleaned_churn.csv"

    try:
        df = load_dataset(input_path)
        display_dataset_info(df)
        check_missing_and_duplicates(df)

        df = clean_total_charges(df)
        df = convert_senior_citizen(df)
        df = clean_columns(df)
        df = remove_duplicates(df)

        print("\nFinal dataset shape after cleaning:", df.shape)
        save_cleaned_dataset(df, output_path)

    except Exception as error:
        print(f"Error during preprocessing: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
