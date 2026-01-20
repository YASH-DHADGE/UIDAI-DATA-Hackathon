

import pandas as pd
import numpy as np
import os
from pathlib import Path
import glob

# Configuration
BASE_DIR = Path(__file__).parent
ENROLMENT_DIR = BASE_DIR / "api_data_aadhar_enrolment" / "api_data_aadhar_enrolment"
DEMOGRAPHIC_DIR = BASE_DIR / "api_data_aadhar_demographic" / "api_data_aadhar_demographic"
BIOMETRIC_DIR = BASE_DIR / "api_data_aadhar_biometric" / "api_data_aadhar_biometric"
OUTPUT_DIR = BASE_DIR / "cleaned_data"

# Column names
DATE_COL = "date"
PINCODE_COL = "pincode"


def load_all_chunks(directory: Path, pattern: str = "*.csv") -> pd.DataFrame:
    """Load and concatenate all CSV chunks from a directory."""
    csv_files = sorted(glob.glob(str(directory / pattern)))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {directory}")
    
    print(f"  Loading {len(csv_files)} file(s) from {directory.name}...")
    dfs = []
    for f in csv_files:
        df = pd.read_csv(f)
        dfs.append(df)
        print(f"    - {Path(f).name}: {len(df):,} rows")
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined


def standardize_date(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Standardize date format to string for consistent comparison."""
    df = df.copy()
    # Keep date as string for intersection (avoid datetime parsing issues)
    df[date_col] = df[date_col].astype(str).str.strip()
    return df


def standardize_pincode(df: pd.DataFrame, pincode_col: str) -> pd.DataFrame:
    """Standardize pincode to consistent format."""
    df = df.copy()
    # Convert to string and remove any decimal points (e.g., 110001.0 -> 110001)
    df[pincode_col] = df[pincode_col].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    return df


def main():
    print("=" * 70)
    print("Data Cleaning - Synchronize Dates and Pincodes Across Three Datasets")
    print("=" * 70)
    
    # Step 1: Load All Three Datasets
    print("\n[Step 1] Loading datasets...")
    
    enrolment_df = load_all_chunks(ENROLMENT_DIR)
    demographic_df = load_all_chunks(DEMOGRAPHIC_DIR)
    biometric_df = load_all_chunks(BIOMETRIC_DIR)
    
    print("\nInitial Dataset Shapes:")
    print(f"  Enrolment:   {enrolment_df.shape[0]:>10,} rows x {enrolment_df.shape[1]} columns")
    print(f"  Demographic: {demographic_df.shape[0]:>10,} rows x {demographic_df.shape[1]} columns")
    print(f"  Biometric:   {biometric_df.shape[0]:>10,} rows x {biometric_df.shape[1]} columns")
    
    
    # Step 2: Standardize Date and Pincode Formats
    
    print("\n[Step 2] Standardizing date and pincode formats...")
    
    enrolment_df = standardize_date(enrolment_df, DATE_COL)
    enrolment_df = standardize_pincode(enrolment_df, PINCODE_COL)
    
    demographic_df = standardize_date(demographic_df, DATE_COL)
    demographic_df = standardize_pincode(demographic_df, PINCODE_COL)
    
    biometric_df = standardize_date(biometric_df, DATE_COL)
    biometric_df = standardize_pincode(biometric_df, PINCODE_COL)
    
    print("  Done.")
    
    # Step 3: Find Common Dates Across All Three Datasets
    print("\n[Step 3] Finding common dates across all datasets...")
    
    enrolment_dates = set(enrolment_df[DATE_COL].dropna().unique())
    demographic_dates = set(demographic_df[DATE_COL].dropna().unique())
    biometric_dates = set(biometric_df[DATE_COL].dropna().unique())
    
    common_dates = enrolment_dates.intersection(demographic_dates).intersection(biometric_dates)
    
    print(f"  Unique dates in Enrolment:   {len(enrolment_dates):,}")
    print(f"  Unique dates in Demographic: {len(demographic_dates):,}")
    print(f"  Unique dates in Biometric:   {len(biometric_dates):,}")
    print(f"  Common dates across all:     {len(common_dates):,}")
    
    # Step 4: Find Common Pincodes Across All Three Datasets
    print("\n[Step 4] Finding common pincodes across all datasets...")
    
    enrolment_pincodes = set(enrolment_df[PINCODE_COL].dropna().unique())
    demographic_pincodes = set(demographic_df[PINCODE_COL].dropna().unique())
    biometric_pincodes = set(biometric_df[PINCODE_COL].dropna().unique())
    
    common_pincodes = enrolment_pincodes.intersection(demographic_pincodes).intersection(biometric_pincodes)
    
    print(f"  Unique pincodes in Enrolment:   {len(enrolment_pincodes):,}")
    print(f"  Unique pincodes in Demographic: {len(demographic_pincodes):,}")
    print(f"  Unique pincodes in Biometric:   {len(biometric_pincodes):,}")
    print(f"  Common pincodes across all:     {len(common_pincodes):,}")
    
    # Step 5: Filter All Datasets to Keep Only Common Dates and Pincodes
    print("\n[Step 5] Filtering datasets to keep only common dates and pincodes...")
    
    enrolment_clean = enrolment_df[
        (enrolment_df[DATE_COL].isin(common_dates)) & 
        (enrolment_df[PINCODE_COL].isin(common_pincodes))
    ].copy()
    
    demographic_clean = demographic_df[
        (demographic_df[DATE_COL].isin(common_dates)) & 
        (demographic_df[PINCODE_COL].isin(common_pincodes))
    ].copy()
    
    biometric_clean = biometric_df[
        (biometric_df[DATE_COL].isin(common_dates)) & 
        (biometric_df[PINCODE_COL].isin(common_pincodes))
    ].copy()
    
    print("\nCleaned Dataset Shapes:")
    print(f"  Enrolment:   {enrolment_clean.shape[0]:>10,} rows (removed {enrolment_df.shape[0] - enrolment_clean.shape[0]:,} rows)")
    print(f"  Demographic: {demographic_clean.shape[0]:>10,} rows (removed {demographic_df.shape[0] - demographic_clean.shape[0]:,} rows)")
    print(f"  Biometric:   {biometric_clean.shape[0]:>10,} rows (removed {biometric_df.shape[0] - biometric_clean.shape[0]:,} rows)")
    
    # Step 6: Verify Data Consistency
    print("\n[Step 6] Verifying data consistency...")
    
    clean_enrol_dates = set(enrolment_clean[DATE_COL].unique())
    clean_demo_dates = set(demographic_clean[DATE_COL].unique())
    clean_bio_dates = set(biometric_clean[DATE_COL].unique())
    
    clean_enrol_pins = set(enrolment_clean[PINCODE_COL].unique())
    clean_demo_pins = set(demographic_clean[PINCODE_COL].unique())
    clean_bio_pins = set(biometric_clean[PINCODE_COL].unique())
    
    dates_match = clean_enrol_dates == clean_demo_dates == clean_bio_dates
    pins_match = clean_enrol_pins == clean_demo_pins == clean_bio_pins
    
    print(f"  Unique dates in cleaned Enrolment:   {len(clean_enrol_dates):,}")
    print(f"  Unique dates in cleaned Demographic: {len(clean_demo_dates):,}")
    print(f"  Unique dates in cleaned Biometric:   {len(clean_bio_dates):,}")
    print(f"  Dates match across all datasets:     {'✓ YES' if dates_match else '✗ NO'}")
    
    print(f"\n  Unique pincodes in cleaned Enrolment:   {len(clean_enrol_pins):,}")
    print(f"  Unique pincodes in cleaned Demographic: {len(clean_demo_pins):,}")
    print(f"  Unique pincodes in cleaned Biometric:   {len(clean_bio_pins):,}")
    print(f"  Pincodes match across all datasets:     {'✓ YES' if pins_match else '✗ NO'}")
    
    # Step 7: Save Cleaned Datasets
    print("\n[Step 7] Saving cleaned datasets...")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    enrolment_clean.to_csv(OUTPUT_DIR / "enrolment_cleaned.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR / 'enrolment_cleaned.csv'}")
    
    demographic_clean.to_csv(OUTPUT_DIR / "demographic_cleaned.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR / 'demographic_cleaned.csv'}")
    
    biometric_clean.to_csv(OUTPUT_DIR / "biometric_cleaned.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR / 'biometric_cleaned.csv'}")
    
    # Step 8: Generate Cleaning Report Summary
    print("\n[Step 8] Generating cleaning summary report...")
    
    original_rows = [enrolment_df.shape[0], demographic_df.shape[0], biometric_df.shape[0]]
    cleaned_rows = [enrolment_clean.shape[0], demographic_clean.shape[0], biometric_clean.shape[0]]
    
    cleaning_report = {
        'Dataset': ['Enrolment', 'Demographic', 'Biometric'],
        'Original_Rows': original_rows,
        'Cleaned_Rows': cleaned_rows,
        'Rows_Removed': [o - c for o, c in zip(original_rows, cleaned_rows)],
        'Removal_Percentage': [
            round((1 - c / o) * 100, 2) if o > 0 else 0 
            for o, c in zip(original_rows, cleaned_rows)
        ]
    }
    
    cleaning_summary = pd.DataFrame(cleaning_report)
    
    print("\nData Cleaning Summary:")
    print(cleaning_summary.to_string(index=False))
    
    cleaning_summary.to_csv(OUTPUT_DIR / "cleaning_summary.csv", index=False)
    print(f"\n  Saved: {OUTPUT_DIR / 'cleaning_summary.csv'}")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("CLEANING COMPLETE!")
    print("=" * 70)
    print(f"\nOutput files saved to: {OUTPUT_DIR}")
    print(f"  - enrolment_cleaned.csv")
    print(f"  - demographic_cleaned.csv")
    print(f"  - biometric_cleaned.csv")
    print(f"  - cleaning_summary.csv")
    print(f"\nCommon dates:    {len(common_dates):,}")
    print(f"Common pincodes: {len(common_pincodes):,}")
    
    return enrolment_clean, demographic_clean, biometric_clean, cleaning_summary


if __name__ == "__main__":
    main()
