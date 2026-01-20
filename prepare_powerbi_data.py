"""
Create aggregated datasets optimized for Power BI visualization.
Generates smaller, pre-aggregated CSV files for efficient dashboard loading.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Setup paths
PROJECT_ROOT = Path('.')
DATA_DIR = PROJECT_ROOT / 'cleaned_data'
POWERBI_DIR = PROJECT_ROOT / 'powerbi_data'
POWERBI_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("CREATING POWER BI OPTIMIZED DATASETS")
print("=" * 60)

# Load cleaned data
print("\n[1/5] Loading cleaned datasets...")
bio_df = pd.read_csv(DATA_DIR / 'biometric_cleaned.csv')
demo_df = pd.read_csv(DATA_DIR / 'demographic_cleaned.csv')
enrol_df = pd.read_csv(DATA_DIR / 'enrolment_cleaned.csv')

# Convert dates
bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y', errors='coerce')
demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y', errors='coerce')
enrol_df['date'] = pd.to_datetime(enrol_df['date'], format='%d-%m-%Y', errors='coerce')

print(f"  Biometric: {len(bio_df):,} rows")
print(f"  Demographic: {len(demo_df):,} rows")
print(f"  Enrolment: {len(enrol_df):,} rows")

# ============================================================================
# 1. DAILY NATIONAL SUMMARY
# ============================================================================
print("\n[2/5] Creating daily national summary...")

# Calculate totals per row
bio_df['bio_total'] = bio_df[[c for c in bio_df.columns if 'age' in c.lower()]].sum(axis=1)
demo_df['demo_total'] = demo_df[[c for c in demo_df.columns if 'age' in c.lower()]].sum(axis=1)
enrol_df['enrol_total'] = enrol_df[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)
enrol_df['child_count'] = enrol_df['age_0_5'] + enrol_df['age_5_17']
enrol_df['adult_count'] = enrol_df['age_18_greater']

daily_bio = bio_df.groupby('date').agg({'bio_total': 'sum'}).reset_index()
daily_demo = demo_df.groupby('date').agg({'demo_total': 'sum'}).reset_index()
daily_enrol = enrol_df.groupby('date').agg({
    'enrol_total': 'sum',
    'child_count': 'sum',
    'adult_count': 'sum'
}).reset_index()

daily_summary = daily_bio.merge(daily_demo, on='date', how='outer')
daily_summary = daily_summary.merge(daily_enrol, on='date', how='outer')
daily_summary = daily_summary.fillna(0).sort_values('date')

# Add time dimensions
daily_summary['year'] = daily_summary['date'].dt.year
daily_summary['month'] = daily_summary['date'].dt.month
daily_summary['month_name'] = daily_summary['date'].dt.month_name()
daily_summary['day'] = daily_summary['date'].dt.day
daily_summary['weekday'] = daily_summary['date'].dt.dayofweek
daily_summary['day_name'] = daily_summary['date'].dt.day_name()
daily_summary['is_weekend'] = daily_summary['weekday'].isin([5, 6]).astype(int)
daily_summary['week_num'] = daily_summary['date'].dt.isocalendar().week

daily_summary.to_csv(POWERBI_DIR / 'daily_national_summary.csv', index=False)
print(f"  Saved: daily_national_summary.csv ({len(daily_summary)} rows)")

# ============================================================================
# 2. STATE-WISE SUMMARY
# ============================================================================
print("\n[3/5] Creating state-wise summary...")

state_bio = bio_df.groupby('state').agg({'bio_total': 'sum'}).reset_index()
state_bio.columns = ['state', 'biometric_total']

state_demo = demo_df.groupby('state').agg({'demo_total': 'sum'}).reset_index()
state_demo.columns = ['state', 'demographic_total']

state_enrol = enrol_df.groupby('state').agg({
    'enrol_total': 'sum',
    'child_count': 'sum',
    'adult_count': 'sum'
}).reset_index()
state_enrol.columns = ['state', 'enrolment_total', 'child_enrolment', 'adult_enrolment']

state_summary = state_bio.merge(state_demo, on='state', how='outer')
state_summary = state_summary.merge(state_enrol, on='state', how='outer')
state_summary = state_summary.fillna(0)

# Calculate metrics
state_summary['total_activity'] = state_summary['biometric_total'] + state_summary['demographic_total'] + state_summary['enrolment_total']
state_summary['bio_coverage_pct'] = (state_summary['biometric_total'] / state_summary['enrolment_total'].replace(0, np.nan) * 100).round(2)
state_summary['child_share_pct'] = (state_summary['child_enrolment'] / state_summary['enrolment_total'].replace(0, np.nan) * 100).round(2)

state_summary = state_summary.sort_values('total_activity', ascending=False)
state_summary.to_csv(POWERBI_DIR / 'state_summary.csv', index=False)
print(f"  Saved: state_summary.csv ({len(state_summary)} rows)")

# ============================================================================
# 3. DISTRICT-WISE SUMMARY
# ============================================================================
print("\n[4/5] Creating district-wise summary...")

# Create region identifier
bio_df['region'] = bio_df['state'].str.strip().str.upper() + ' - ' + bio_df['district'].str.strip().str.upper()
demo_df['region'] = demo_df['state'].str.strip().str.upper() + ' - ' + demo_df['district'].str.strip().str.upper()
enrol_df['region'] = enrol_df['state'].str.strip().str.upper() + ' - ' + enrol_df['district'].str.strip().str.upper()

region_bio = bio_df.groupby(['state', 'district', 'region']).agg({'bio_total': 'sum'}).reset_index()
region_bio.columns = ['state', 'district', 'region', 'biometric_total']

region_demo = demo_df.groupby(['state', 'district', 'region']).agg({'demo_total': 'sum'}).reset_index()
region_demo.columns = ['state', 'district', 'region', 'demographic_total']

region_enrol = enrol_df.groupby(['state', 'district', 'region']).agg({
    'enrol_total': 'sum',
    'child_count': 'sum',
    'adult_count': 'sum'
}).reset_index()
region_enrol.columns = ['state', 'district', 'region', 'enrolment_total', 'child_enrolment', 'adult_enrolment']

district_summary = region_bio.merge(region_demo, on=['state', 'district', 'region'], how='outer')
district_summary = district_summary.merge(region_enrol, on=['state', 'district', 'region'], how='outer')
district_summary = district_summary.fillna(0)

# Calculate metrics
district_summary['total_activity'] = district_summary['biometric_total'] + district_summary['demographic_total'] + district_summary['enrolment_total']
district_summary['bio_coverage_pct'] = (district_summary['biometric_total'] / district_summary['enrolment_total'].replace(0, np.nan) * 100).round(2)
district_summary['child_share_pct'] = (district_summary['child_enrolment'] / district_summary['enrolment_total'].replace(0, np.nan) * 100).round(2)

district_summary = district_summary.sort_values('total_activity', ascending=False)
district_summary.to_csv(POWERBI_DIR / 'district_summary.csv', index=False)
print(f"  Saved: district_summary.csv ({len(district_summary)} rows)")

# ============================================================================
# 4. STATE-DATE COMBINATION (for trends by state)
# ============================================================================
print("\n[5/5] Creating state-date trends...")

state_date_bio = bio_df.groupby(['state', 'date']).agg({'bio_total': 'sum'}).reset_index()
state_date_demo = demo_df.groupby(['state', 'date']).agg({'demo_total': 'sum'}).reset_index()
state_date_enrol = enrol_df.groupby(['state', 'date']).agg({'enrol_total': 'sum'}).reset_index()

state_date = state_date_bio.merge(state_date_demo, on=['state', 'date'], how='outer')
state_date = state_date.merge(state_date_enrol, on=['state', 'date'], how='outer')
state_date = state_date.fillna(0)

state_date.columns = ['state', 'date', 'biometric', 'demographic', 'enrolment']
state_date['total'] = state_date['biometric'] + state_date['demographic'] + state_date['enrolment']
state_date = state_date.sort_values(['state', 'date'])

state_date.to_csv(POWERBI_DIR / 'state_date_trends.csv', index=False)
print(f"  Saved: state_date_trends.csv ({len(state_date)} rows)")

# ============================================================================
# 5. COPY INSIGHT FILES
# ============================================================================
print("\n[6/6] Copying insight files...")

import shutil

# Copy key insight CSVs
insight_files = [
    'outputs/top_1_percent_enrolment_regions.csv',
    'outputs/lowest_biometric_coverage_regions.csv',
    'outputs/low_child_penetration_regions.csv',
    'outputs/high_adult_only_demographic_regions.csv',
    'outputs/delayed_biometric_completion_regions.csv',
    'outputs/high_variance_regions.csv',
    'cleaned_data/suspicious_pincodes_misuse.csv',
    'cleaned_data/imbalanced_pincodes.csv',
]

for f in insight_files:
    src = PROJECT_ROOT / f
    if src.exists():
        dst = POWERBI_DIR / src.name
        shutil.copy(src, dst)
        print(f"  Copied: {src.name}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("POWER BI DATA PREPARATION COMPLETE")
print("=" * 60)
print(f"\nOutput Directory: {POWERBI_DIR.absolute()}")
print("\nFiles created for Power BI:")
for f in sorted(POWERBI_DIR.glob('*.csv')):
    size = f.stat().st_size / 1024
    print(f"  {f.name:45} {size:>8.1f} KB")

print("\n✓ Data ready for Power BI import!")
