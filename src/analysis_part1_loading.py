"""
UIDAI Data Hackathon 2026 - Aadhaar Data Analysis
Comprehensive analysis of anonymized Aadhaar enrolment and update datasets

Author: UIDAI Data Hackathon 2026 Participant
Date: January 2026
"""

# =============================================================================
# 1. IMPORTS AND SETUP
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os
from datetime import datetime
from pathlib import Path

# Configuration
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# Set random seed for reproducibility
np.random.seed(42)

# Create output directory
VISUALIZATIONS_DIR = Path('../visualizations')
VISUALIZATIONS_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("UIDAI DATA HACKATHON 2026")
print("Aadhaar Data Analysis - Comprehensive Report")
print("=" * 60)
print(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# =============================================================================
# 2. DATA LOADING
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 1: DATA LOADING")
print("=" * 60)

def load_dataset(folder_name, dataset_type):
    """Load and concatenate all CSV chunks for a dataset type."""
    base_path = Path(f'../{folder_name}/{folder_name}')
    all_files = list(base_path.glob('*.csv'))
    
    if not all_files:
        print(f"Warning: No files found in {base_path}")
        return pd.DataFrame()
    
    dfs = []
    for f in sorted(all_files):
        try:
            df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip')
        except:
            df = pd.read_csv(f, encoding='latin-1', on_bad_lines='skip')
        dfs.append(df)
        print(f"  Loaded: {f.name} ({len(df):,} rows)")
    
    combined = pd.concat(dfs, ignore_index=True)
    print(f"  Total {dataset_type}: {len(combined):,} rows")
    return combined

print("\n📊 Loading Biometric Update Data...")
df_biometric = load_dataset('api_data_aadhar_biometric', 'Biometric')

print("\n📊 Loading Demographic Update Data...")
df_demographic = load_dataset('api_data_aadhar_demographic', 'Demographic')

print("\n📊 Loading Enrolment Data...")
df_enrolment = load_dataset('api_data_aadhar_enrolment', 'Enrolment')

# =============================================================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 2: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

def dataset_overview(df, name):
    """Generate comprehensive overview of a dataset."""
    print(f"\n{'='*40}")
    print(f"📋 {name} Dataset Overview")
    print(f"{'='*40}")
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nSample Data:")
    print(df.head(3).to_string())
    return df

df_biometric = dataset_overview(df_biometric, "Biometric")
df_demographic = dataset_overview(df_demographic, "Demographic")
df_enrolment = dataset_overview(df_enrolment, "Enrolment")
