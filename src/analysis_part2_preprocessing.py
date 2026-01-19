# =============================================================================
# 4. DATA PREPROCESSING
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 3: DATA PREPROCESSING")
print("=" * 60)

def preprocess_dataset(df, name):
    """Clean and preprocess a dataset."""
    print(f"\n🔧 Preprocessing {name}...")
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Extract temporal features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.dayofweek
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['day_name'] = df['date'].dt.day_name()
    df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)
    
    # Calculate total updates/enrolments per row
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    age_cols = [c for c in numeric_cols if 'age' in c.lower() or 'bio' in c.lower() or 'demo' in c.lower()]
    if age_cols:
        df['total_count'] = df[age_cols].sum(axis=1)
    
    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"  Removed {before - after:,} duplicate rows")
    
    # Handle missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        df = df.dropna()
        print(f"  Removed {missing:,} rows with missing values")
    
    print(f"  Final shape: {df.shape}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df

df_biometric = preprocess_dataset(df_biometric, "Biometric")
df_demographic = preprocess_dataset(df_demographic, "Demographic")
df_enrolment = preprocess_dataset(df_enrolment, "Enrolment")

# Standardize state names (remove extra spaces, lowercase for matching)
for df in [df_biometric, df_demographic, df_enrolment]:
    df['state_clean'] = df['state'].str.strip().str.title()
    df['district_clean'] = df['district'].str.strip().str.title()

print("\n✅ Preprocessing Complete!")

# =============================================================================
# 5. UNIVARIATE ANALYSIS
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 4: UNIVARIATE ANALYSIS")
print("=" * 60)

def statistical_summary(df, name, numeric_cols):
    """Generate detailed statistical summary."""
    print(f"\n📊 Statistical Summary: {name}")
    stats_df = df[numeric_cols].describe().T
    stats_df['median'] = df[numeric_cols].median()
    stats_df['skewness'] = df[numeric_cols].skew()
    stats_df['kurtosis'] = df[numeric_cols].kurtosis()
    print(stats_df.round(2).to_string())
    return stats_df

# Get numeric columns for each dataset
bio_numeric = [c for c in df_biometric.columns if df_biometric[c].dtype in ['int64', 'float64'] and c not in ['year', 'month', 'day', 'weekday', 'week_of_year', 'is_weekend']]
demo_numeric = [c for c in df_demographic.columns if df_demographic[c].dtype in ['int64', 'float64'] and c not in ['year', 'month', 'day', 'weekday', 'week_of_year', 'is_weekend']]
enrol_numeric = [c for c in df_enrolment.columns if df_enrolment[c].dtype in ['int64', 'float64'] and c not in ['year', 'month', 'day', 'weekday', 'week_of_year', 'is_weekend']]

stats_bio = statistical_summary(df_biometric, "Biometric Updates", bio_numeric)
stats_demo = statistical_summary(df_demographic, "Demographic Updates", demo_numeric)
stats_enrol = statistical_summary(df_enrolment, "Enrolments", enrol_numeric)

# Outlier Detection using IQR
def detect_outliers_iqr(df, col):
    """Detect outliers using IQR method."""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    return len(outliers), lower, upper

print("\n🔍 Outlier Detection (IQR Method)")
for name, df, cols in [("Biometric", df_biometric, ['total_count']), 
                        ("Demographic", df_demographic, ['total_count']),
                        ("Enrolment", df_enrolment, ['total_count'])]:
    for col in cols:
        if col in df.columns:
            n_outliers, lower, upper = detect_outliers_iqr(df, col)
            print(f"  {name} - {col}: {n_outliers:,} outliers (bounds: {lower:.1f} to {upper:.1f})")
