# UIDAI Data Analysis - Using Cleaned Data
# ==========================================
# This script analyzes the synchronized cleaned datasets.
# Run: python notebooks/uidai_analysis.py
# Or convert to notebook: jupytext --to notebook uidai_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
from datetime import datetime
import warnings
import os

# Setup
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
np.random.seed(42)

# Paths - Updated to use cleaned data (works in both script and notebook)
# Handle both script (__file__ available) and notebook (use cwd) environments
try:
    PROJECT_ROOT = Path(__file__).parent.parent
except NameError:
    # Running in Jupyter notebook - use current directory
    PROJECT_ROOT = Path.cwd()
    if PROJECT_ROOT.name == 'notebooks':
        PROJECT_ROOT = PROJECT_ROOT.parent

DATA_DIR = PROJECT_ROOT / 'cleaned_data'
VIS_DIR = PROJECT_ROOT / 'visualizations'
VIS_DIR.mkdir(exist_ok=True)

# Colors
COLORS = {'bio': '#7B1FA2', 'demo': '#00897B', 'enrol': '#D81B60', 'primary': '#1E88E5'}

print("=" * 70)
print("UIDAI DATA HACKATHON 2026 - AADHAAR DATA ANALYSIS")
print("Using Synchronized Cleaned Datasets")
print("=" * 70)
print(f"Analysis Date: {datetime.now()}")
print(f"Data Directory: {DATA_DIR}")
print(f"Output Directory: {VIS_DIR}")

# =============================================================================
# 1. DATA LOADING - Using cleaned data files
# =============================================================================
print("\n[1/10] LOADING CLEANED DATA...")

df_bio = pd.read_csv(DATA_DIR / 'biometric_cleaned.csv')
df_demo = pd.read_csv(DATA_DIR / 'demographic_cleaned.csv')
df_enrol = pd.read_csv(DATA_DIR / 'enrolment_cleaned.csv')

print(f"\n✓ Biometric: {len(df_bio):,} rows")
print(f"✓ Demographic: {len(df_demo):,} rows")
print(f"✓ Enrolment: {len(df_enrol):,} rows")
print(f"\nNote: Data is already synchronized (common dates & pincodes only)")

# =============================================================================
# 2. PREPROCESSING
# =============================================================================
print("\n[2/10] PREPROCESSING...")

def preprocess(df, name):
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.dayofweek
    df['day_name'] = df['date'].dt.day_name()
    df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)
    df['state_clean'] = df['state'].str.strip().str.title()
    
    # Total count per row
    num_cols = df.select_dtypes(include=[np.number]).columns
    age_cols = [c for c in num_cols if 'age' in c.lower() or 'bio' in c.lower() or 'demo' in c.lower()]
    if age_cols:
        df['total_count'] = df[age_cols].sum(axis=1)
    
    df = df.drop_duplicates().dropna(subset=['date'])
    print(f"  {name}: {len(df):,} rows after cleaning")
    return df

df_bio = preprocess(df_bio, "Biometric")
df_demo = preprocess(df_demo, "Demographic")
df_enrol = preprocess(df_enrol, "Enrolment")

# =============================================================================
# 3. STATISTICAL SUMMARY
# =============================================================================
print("\n[3/10] STATISTICAL SUMMARY...")

for name, df in [("Biometric", df_bio), ("Demographic", df_demo), ("Enrolment", df_enrol)]:
    print(f"\n{name} - total_count stats:")
    print(f"  Mean: {df['total_count'].mean():,.1f}")
    print(f"  Median: {df['total_count'].median():,.1f}")
    print(f"  Std: {df['total_count'].std():,.1f}")
    print(f"  Min/Max: {df['total_count'].min():,.0f} / {df['total_count'].max():,.0f}")

# =============================================================================
# 4. VISUALIZATION 1: Time Series
# =============================================================================
print("\n[4/10] CREATING TIME SERIES PLOTS...")

fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

for ax, (name, df, color) in zip(axes, [('Biometric', df_bio, COLORS['bio']), 
                                          ('Demographic', df_demo, COLORS['demo']),
                                          ('Enrolment', df_enrol, COLORS['enrol'])]):
    daily = df.groupby('date')['total_count'].sum()
    ax.fill_between(daily.index, daily.values, alpha=0.4, color=color)
    ax.plot(daily.index, daily.values, color=color, linewidth=1)
    ax.axhline(daily.mean(), color='red', linestyle='--', alpha=0.7, label=f'Mean: {daily.mean():,.0f}')
    ax.set_title(f'Daily {name} Activity', fontweight='bold')
    ax.set_ylabel('Count')
    ax.legend()

plt.xlabel('Date')
plt.suptitle('UIDAI Aadhaar Activity Over Time (Cleaned Data)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / '01_time_series.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 01_time_series.png")

# =============================================================================
# 5. VISUALIZATION 2: Top States
# =============================================================================
print("\n[5/10] CREATING STATE DISTRIBUTION...")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, (name, df, color) in zip(axes, [('Biometric', df_bio, COLORS['bio']),
                                          ('Demographic', df_demo, COLORS['demo']),
                                          ('Enrolment', df_enrol, COLORS['enrol'])]):
    top = df.groupby('state_clean')['total_count'].sum().nlargest(15)
    ax.barh(top.index, top.values / 1e6, color=color, alpha=0.8)
    ax.set_title(f'Top 15 States - {name}', fontweight='bold')
    ax.set_xlabel('Total (Millions)')

plt.suptitle('State-wise Aadhaar Activity', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / '02_states.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 02_states.png")

# =============================================================================
# 6. VISUALIZATION 3: Day of Week
# =============================================================================
print("\n[6/10] CREATING DAY OF WEEK ANALYSIS...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for ax, (name, df, color) in zip(axes, [('Biometric', df_bio, COLORS['bio']),
                                          ('Demographic', df_demo, COLORS['demo']),
                                          ('Enrolment', df_enrol, COLORS['enrol'])]):
    dow = df.groupby('day_name')['total_count'].mean().reindex(day_order)
    bars = ax.bar(dow.index, dow.values, color=color, alpha=0.8)
    for i, d in enumerate(day_order):
        if d in ['Saturday', 'Sunday']:
            bars[i].set_alpha(0.4)
            bars[i].set_hatch('//')
    ax.set_title(f'{name} by Day', fontweight='bold')
    ax.tick_params(axis='x', rotation=45)

plt.suptitle('Activity by Day of Week (Weekends Hatched)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / '03_weekday.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 03_weekday.png")

# =============================================================================
# 7. VISUALIZATION 4: Age Distribution
# =============================================================================
print("\n[7/10] CREATING AGE DISTRIBUTION...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

enrol_age = [c for c in df_enrol.columns if 'age' in c.lower() and c != 'total_count']
bio_age = [c for c in df_bio.columns if 'bio_age' in c.lower()]
demo_age = [c for c in df_demo.columns if 'demo_age' in c.lower()]

for ax, (name, df, cols) in zip(axes, [('Biometric', df_bio, bio_age),
                                         ('Demographic', df_demo, demo_age),
                                         ('Enrolment', df_enrol, enrol_age)]):
    if cols:
        totals = df[cols].sum()
        labels = [c.replace('bio_', '').replace('demo_', '').replace('_', ' ').title() for c in cols]
        ax.pie(totals.values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(f'{name} - Age Groups', fontweight='bold')

plt.suptitle('Age Group Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / '04_age_dist.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 04_age_dist.png")

# =============================================================================
# 8. VISUALIZATION 5: Correlation & Box Plots
# =============================================================================
print("\n[8/10] CREATING CORRELATION & BOX PLOTS...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Box plots (top row)
for ax, (name, df, color) in zip(axes[0], [('Biometric', df_bio, COLORS['bio']),
                                            ('Demographic', df_demo, COLORS['demo']),
                                            ('Enrolment', df_enrol, COLORS['enrol'])]):
    bp = ax.boxplot(df['total_count'].values, patch_artist=True)
    bp['boxes'][0].set_facecolor(color)
    ax.set_title(f'{name} Distribution', fontweight='bold')
    ax.set_ylabel('Count')

# State comparison (bottom left)
state_comp = pd.DataFrame({
    'Biometric': df_bio.groupby('state_clean')['total_count'].sum(),
    'Demographic': df_demo.groupby('state_clean')['total_count'].sum()
}).dropna()
axes[1,0].scatter(state_comp['Biometric']/1e6, state_comp['Demographic']/1e6, alpha=0.6, c=COLORS['primary'])
axes[1,0].set_xlabel('Biometric (M)')
axes[1,0].set_ylabel('Demographic (M)')
axes[1,0].set_title('State Correlation: Bio vs Demo', fontweight='bold')
corr = state_comp['Biometric'].corr(state_comp['Demographic'])
axes[1,0].text(0.05, 0.95, f'r = {corr:.3f}', transform=axes[1,0].transAxes, fontsize=12, va='top')

# Weekday heatmap (bottom middle)
pivot = df_bio.pivot_table(values='total_count', index='weekday', 
                            columns=df_bio['date'].dt.to_period('W'), aggfunc='sum')
if not pivot.empty:
    sns.heatmap(pivot.iloc[:, :10], cmap='Purples', ax=axes[1,1], cbar_kws={'label': 'Count'})
    axes[1,1].set_title('Biometric Weekly Heatmap', fontweight='bold')
    axes[1,1].set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

# Monthly trend (bottom right)
monthly = df_enrol.groupby(df_enrol['date'].dt.to_period('M'))['total_count'].sum()
axes[1,2].bar(range(len(monthly)), monthly.values/1e6, color=COLORS['enrol'])
axes[1,2].set_title('Monthly Enrolments', fontweight='bold')
axes[1,2].set_xlabel('Month')
axes[1,2].set_ylabel('Total (M)')

plt.tight_layout()
plt.savefig(VIS_DIR / '05_analysis_grid.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 05_analysis_grid.png")

# =============================================================================
# 9. ANOMALY DETECTION
# =============================================================================
print("\n[9/10] ANOMALY DETECTION...")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (name, df, color) in zip(axes, [('Biometric', df_bio, COLORS['bio']),
                                          ('Demographic', df_demo, COLORS['demo']),
                                          ('Enrolment', df_enrol, COLORS['enrol'])]):
    daily = df.groupby('date')['total_count'].sum()
    z_scores = np.abs(stats.zscore(daily.values))
    anomalies = daily[z_scores > 2.5]
    
    ax.plot(daily.index, daily.values, color=color, alpha=0.7)
    ax.scatter(anomalies.index, anomalies.values, color='red', s=80, zorder=5, 
               label=f'{len(anomalies)} anomalies')
    ax.axhline(daily.mean(), color='green', linestyle='--', alpha=0.7)
    ax.set_title(f'{name} Anomalies', fontweight='bold')
    ax.legend()

plt.suptitle('Anomaly Detection (Z-Score > 2.5)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VIS_DIR / '06_anomalies.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 06_anomalies.png")

# =============================================================================
# 10. EXECUTIVE DASHBOARD
# =============================================================================
print("\n[10/10] CREATING EXECUTIVE DASHBOARD...")

fig = plt.figure(figsize=(20, 14))

# Totals summary
ax1 = fig.add_subplot(2, 3, 1)
totals = [df_bio['total_count'].sum()/1e6, df_demo['total_count'].sum()/1e6, df_enrol['total_count'].sum()/1e6]
bars = ax1.bar(['Biometric', 'Demographic', 'Enrolment'], totals, 
               color=[COLORS['bio'], COLORS['demo'], COLORS['enrol']])
ax1.set_title('Total Activity (Millions)', fontweight='bold')
ax1.set_ylabel('Count (M)')
for bar, val in zip(bars, totals):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f'{val:.1f}M', ha='center', fontweight='bold')

# Top 5 states combined
ax2 = fig.add_subplot(2, 3, 2)
combined = df_bio.groupby('state_clean')['total_count'].sum() + \
           df_demo.groupby('state_clean')['total_count'].sum() + \
           df_enrol.groupby('state_clean')['total_count'].sum()
top5 = combined.nlargest(5)
ax2.barh(top5.index, top5.values/1e6, color=COLORS['primary'])
ax2.set_title('Top 5 States (Combined)', fontweight='bold')
ax2.set_xlabel('Total (M)')

# Weekend vs Weekday
ax3 = fig.add_subplot(2, 3, 3)
wd_bio = df_bio[df_bio['is_weekend']==0]['total_count'].mean()
we_bio = df_bio[df_bio['is_weekend']==1]['total_count'].mean()
bars = ax3.bar(['Weekday', 'Weekend'], [wd_bio, we_bio], color=[COLORS['bio'], COLORS['bio']])
bars[1].set_alpha(0.5)
ax3.set_title('Average Daily Activity', fontweight='bold')
pct = (we_bio - wd_bio) / wd_bio * 100
ax3.text(1, we_bio, f'{pct:+.1f}%', ha='center', va='bottom')

# Time trend all datasets
ax4 = fig.add_subplot(2, 1, 2)
bio_d = df_bio.groupby('date')['total_count'].sum()
demo_d = df_demo.groupby('date')['total_count'].sum()
enrol_d = df_enrol.groupby('date')['total_count'].sum()
ax4.plot(bio_d.index, bio_d.values/1e3, label='Biometric', color=COLORS['bio'])
ax4.plot(demo_d.index, demo_d.values/1e3, label='Demographic', color=COLORS['demo'])
ax4.plot(enrol_d.index, enrol_d.values/1e3, label='Enrolment', color=COLORS['enrol'])
ax4.set_title('Daily Activity Trends', fontweight='bold')
ax4.set_xlabel('Date')
ax4.set_ylabel('Count (K)')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle('UIDAI AADHAAR DATA ANALYSIS - EXECUTIVE DASHBOARD\n(Using Synchronized Cleaned Data)', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(VIS_DIR / '07_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Saved 07_dashboard.png")

# =============================================================================
# KEY INSIGHTS
# =============================================================================
print("\n" + "=" * 70)
print("KEY INSIGHTS")
print("=" * 70)

top_bio = df_bio.groupby('state_clean')['total_count'].sum().idxmax()
top_enrol = df_enrol.groupby('state_clean')['total_count'].sum().idxmax()

insights = f"""
1. SCALE: Total {(df_bio['total_count'].sum() + df_demo['total_count'].sum() + df_enrol['total_count'].sum())/1e6:.1f}M Aadhaar activities

2. TOP STATES: 
   - Biometric: {top_bio}
   - Enrolment: {top_enrol}

3. WEEKEND PATTERN: {pct:+.1f}% activity change on weekends

4. CORRELATION: Bio-Demo correlation r={corr:.3f} (strong positive)

5. DATA QUALITY: Using synchronized cleaned data
   - Common dates across all datasets: 70
   - Common pincodes across all datasets: 19,410+

6. RECOMMENDATIONS:
   - Focus resources on high-activity states
   - Consider weekend operations expansion
   - Investigate low-activity regions for accessibility
"""
print(insights)

# Save insights
with open(VIS_DIR / 'KEY_INSIGHTS.txt', 'w') as f:
    f.write(insights)

print("\n" + "=" * 70)
print("✅ ANALYSIS COMPLETE!")
print("=" * 70)
print(f"\n📁 Visualizations saved to: {VIS_DIR}")
print(f"📊 Charts: 7")
print(f"📝 Insights: KEY_INSIGHTS.txt")
