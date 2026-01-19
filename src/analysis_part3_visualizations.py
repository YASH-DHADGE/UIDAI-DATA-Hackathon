# =============================================================================
# 6. VISUALIZATIONS - UNIVARIATE
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 5: UNIVARIATE VISUALIZATIONS")
print("=" * 60)

# Configure plot style
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Color palette
COLORS = {
    'primary': '#1E88E5',
    'secondary': '#43A047',
    'accent': '#E53935',
    'warning': '#FB8C00',
    'info': '#00ACC1',
    'biometric': '#7B1FA2',
    'demographic': '#00897B',
    'enrolment': '#D81B60'
}

# 1. Time Series - Daily Total Activity
print("\n📈 Creating Time Series Visualizations...")

fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# Biometric daily totals
bio_daily = df_biometric.groupby('date')['total_count'].sum()
axes[0].plot(bio_daily.index, bio_daily.values, color=COLORS['biometric'], linewidth=1.5, alpha=0.8)
axes[0].fill_between(bio_daily.index, bio_daily.values, alpha=0.3, color=COLORS['biometric'])
axes[0].set_title('📊 Daily Biometric Updates', fontweight='bold', pad=10)
axes[0].set_ylabel('Total Updates')
axes[0].axhline(bio_daily.mean(), color='red', linestyle='--', alpha=0.7, label=f'Mean: {bio_daily.mean():,.0f}')
axes[0].legend()

# Demographic daily totals
demo_daily = df_demographic.groupby('date')['total_count'].sum()
axes[1].plot(demo_daily.index, demo_daily.values, color=COLORS['demographic'], linewidth=1.5, alpha=0.8)
axes[1].fill_between(demo_daily.index, demo_daily.values, alpha=0.3, color=COLORS['demographic'])
axes[1].set_title('📊 Daily Demographic Updates', fontweight='bold', pad=10)
axes[1].set_ylabel('Total Updates')
axes[1].axhline(demo_daily.mean(), color='red', linestyle='--', alpha=0.7, label=f'Mean: {demo_daily.mean():,.0f}')
axes[1].legend()

# Enrolment daily totals
enrol_daily = df_enrolment.groupby('date')['total_count'].sum()
axes[2].plot(enrol_daily.index, enrol_daily.values, color=COLORS['enrolment'], linewidth=1.5, alpha=0.8)
axes[2].fill_between(enrol_daily.index, enrol_daily.values, alpha=0.3, color=COLORS['enrolment'])
axes[2].set_title('📊 Daily New Enrolments', fontweight='bold', pad=10)
axes[2].set_ylabel('Total Enrolments')
axes[2].set_xlabel('Date')
axes[2].axhline(enrol_daily.mean(), color='red', linestyle='--', alpha=0.7, label=f'Mean: {enrol_daily.mean():,.0f}')
axes[2].legend()

plt.suptitle('UIDAI Aadhaar Activity - Time Series Analysis', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '01_time_series_daily.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 01_time_series_daily.png")

# 2. State-wise Distribution
print("\n📊 Creating State-wise Distribution...")

fig, axes = plt.subplots(1, 3, figsize=(18, 8))

for idx, (name, df, color) in enumerate([
    ('Biometric Updates', df_biometric, COLORS['biometric']),
    ('Demographic Updates', df_demographic, COLORS['demographic']),
    ('Enrolments', df_enrolment, COLORS['enrolment'])
]):
    state_totals = df.groupby('state_clean')['total_count'].sum().sort_values(ascending=True).tail(15)
    axes[idx].barh(state_totals.index, state_totals.values, color=color, alpha=0.8)
    axes[idx].set_title(f'Top 15 States - {name}', fontweight='bold')
    axes[idx].set_xlabel('Total Count')
    # Add value labels
    for i, v in enumerate(state_totals.values):
        axes[idx].text(v + state_totals.max()*0.01, i, f'{v/1e6:.2f}M', va='center', fontsize=8)

plt.suptitle('State-wise Aadhaar Activity Distribution', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '02_state_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 02_state_distribution.png")

# 3. Age Group Distribution
print("\n📊 Creating Age Group Distribution...")

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# Get age-related columns for each dataset
bio_age_cols = [c for c in df_biometric.columns if 'bio_age' in c.lower()]
demo_age_cols = [c for c in df_demographic.columns if 'demo_age' in c.lower()]
enrol_age_cols = [c for c in df_enrolment.columns if 'age' in c.lower() and c != 'total_count']

for idx, (name, df, cols, color) in enumerate([
    ('Biometric', df_biometric, bio_age_cols, COLORS['biometric']),
    ('Demographic', df_demographic, demo_age_cols, COLORS['demographic']),
    ('Enrolment', df_enrolment, enrol_age_cols, COLORS['enrolment'])
]):
    if cols:
        age_totals = df[cols].sum()
        age_totals.index = [c.replace('bio_', '').replace('demo_', '').replace('_', ' ').title() for c in age_totals.index]
        axes[idx].pie(age_totals.values, labels=age_totals.index, autopct='%1.1f%%', 
                      colors=sns.color_palette("husl", len(cols)), startangle=90)
        axes[idx].set_title(f'{name} - Age Distribution', fontweight='bold')

plt.suptitle('Age Group Distribution Across Datasets', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '03_age_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 03_age_distribution.png")

# 4. Box Plots for Outlier Visualization
print("\n📊 Creating Box Plots for Outliers...")

fig, axes = plt.subplots(1, 3, figsize=(15, 6))

for idx, (name, df, color) in enumerate([
    ('Biometric', df_biometric, COLORS['biometric']),
    ('Demographic', df_demographic, COLORS['demographic']),
    ('Enrolment', df_enrolment, COLORS['enrolment'])
]):
    bp = axes[idx].boxplot(df['total_count'].values, patch_artist=True, vert=True)
    bp['boxes'][0].set_facecolor(color)
    bp['boxes'][0].set_alpha(0.7)
    axes[idx].set_title(f'{name} - Total Count Distribution', fontweight='bold')
    axes[idx].set_ylabel('Count per Record')
    
    # Add stats annotation
    stats_text = f"Mean: {df['total_count'].mean():,.0f}\nMedian: {df['total_count'].median():,.0f}\nStd: {df['total_count'].std():,.0f}"
    axes[idx].text(0.95, 0.95, stats_text, transform=axes[idx].transAxes, 
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=9)

plt.suptitle('Distribution of Record-Level Activity (Outlier Detection)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '04_boxplots_outliers.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 04_boxplots_outliers.png")

# 5. Day of Week Analysis
print("\n📊 Creating Day of Week Analysis...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for idx, (name, df, color) in enumerate([
    ('Biometric', df_biometric, COLORS['biometric']),
    ('Demographic', df_demographic, COLORS['demographic']),
    ('Enrolment', df_enrolment, COLORS['enrolment'])
]):
    dow_totals = df.groupby('day_name')['total_count'].mean().reindex(day_order)
    bars = axes[idx].bar(dow_totals.index, dow_totals.values, color=color, alpha=0.8)
    axes[idx].set_title(f'{name} - Avg Daily Activity', fontweight='bold')
    axes[idx].set_ylabel('Average Count')
    axes[idx].tick_params(axis='x', rotation=45)
    
    # Highlight weekends
    for i, day in enumerate(day_order):
        if day in ['Saturday', 'Sunday']:
            bars[i].set_alpha(0.4)
            bars[i].set_hatch('//')

plt.suptitle('Activity by Day of Week (Weekends Hatched)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '05_day_of_week.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 05_day_of_week.png")
