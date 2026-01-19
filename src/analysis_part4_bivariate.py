# =============================================================================
# 7. BIVARIATE ANALYSIS
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 6: BIVARIATE ANALYSIS")
print("=" * 60)

# 6. Correlation Analysis
print("\n📊 Creating Correlation Heatmaps...")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (name, df, color) in enumerate([
    ('Biometric', df_biometric, 'Purples'),
    ('Demographic', df_demographic, 'Greens'),
    ('Enrolment', df_enrolment, 'RdPu')
]):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Remove derived temporal cols for correlation
    corr_cols = [c for c in numeric_cols if c not in ['year', 'month', 'day', 'weekday', 'week_of_year', 'is_weekend']]
    if len(corr_cols) > 1:
        corr = df[corr_cols].corr()
        sns.heatmap(corr, annot=True, cmap=color, center=0, ax=axes[idx], fmt='.2f',
                    square=True, linewidths=0.5)
        axes[idx].set_title(f'{name} - Correlation Matrix', fontweight='bold')

plt.suptitle('Correlation Analysis Between Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '06_correlation_heatmaps.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 06_correlation_heatmaps.png")

# 7. State vs Age Group Cross-tabulation
print("\n📊 Creating State vs Age Group Analysis...")

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Top 10 states for Enrolment by age group
top_states = df_enrolment.groupby('state_clean')['total_count'].sum().nlargest(10).index.tolist()
enrol_filtered = df_enrolment[df_enrolment['state_clean'].isin(top_states)]

# Cross-tab: State vs Age Groups
enrol_age_cols = [c for c in df_enrolment.columns if 'age' in c.lower() and c not in ['total_count']]
if enrol_age_cols:
    state_age = enrol_filtered.groupby('state_clean')[enrol_age_cols].sum()
    state_age.columns = [c.replace('_', ' ').title() for c in state_age.columns]
    state_age.plot(kind='barh', stacked=True, ax=axes[0], colormap='viridis', alpha=0.85)
    axes[0].set_title('Top 10 States - Enrolment by Age Group', fontweight='bold')
    axes[0].set_xlabel('Total Enrolments')
    axes[0].legend(title='Age Group', bbox_to_anchor=(1.02, 1))

# Compare Biometric vs Demographic updates by state
top_states_bio = df_biometric.groupby('state_clean')['total_count'].sum()
top_states_demo = df_demographic.groupby('state_clean')['total_count'].sum()

comparison = pd.DataFrame({
    'Biometric': top_states_bio,
    'Demographic': top_states_demo
}).fillna(0).sort_values('Biometric', ascending=False).head(10)

comparison.plot(kind='barh', ax=axes[1], color=[COLORS['biometric'], COLORS['demographic']], alpha=0.8)
axes[1].set_title('Top 10 States - Biometric vs Demographic Updates', fontweight='bold')
axes[1].set_xlabel('Total Updates')
axes[1].legend(title='Update Type')

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '07_state_age_crosstab.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 07_state_age_crosstab.png")

# 8. Weekend vs Weekday Analysis
print("\n📊 Creating Weekend vs Weekday Comparison...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (name, df, color) in enumerate([
    ('Biometric', df_biometric, COLORS['biometric']),
    ('Demographic', df_demographic, COLORS['demographic']),
    ('Enrolment', df_enrolment, COLORS['enrolment'])
]):
    weekend_data = df.groupby('is_weekend')['total_count'].agg(['mean', 'sum', 'count'])
    weekend_data.index = ['Weekday', 'Weekend']
    
    bars = axes[idx].bar(weekend_data.index, weekend_data['mean'], color=[color, color], alpha=[0.9, 0.5])
    bars[1].set_hatch('//')
    axes[idx].set_title(f'{name} - Avg Activity', fontweight='bold')
    axes[idx].set_ylabel('Average Count per Record')
    
    # Add percentage difference annotation
    pct_diff = ((weekend_data['mean']['Weekend'] - weekend_data['mean']['Weekday']) / weekend_data['mean']['Weekday']) * 100
    axes[idx].annotate(f'{pct_diff:+.1f}% on weekends', xy=(1, weekend_data['mean']['Weekend']),
                       xytext=(0.7, weekend_data['mean'].max()*0.8),
                       arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10)

plt.suptitle('Weekend vs Weekday Activity Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '08_weekend_weekday.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 08_weekend_weekday.png")

# 9. Monthly Trends
print("\n📊 Creating Monthly Trends...")

fig, ax = plt.subplots(figsize=(14, 6))

bio_monthly = df_biometric.groupby(df_biometric['date'].dt.to_period('M'))['total_count'].sum()
demo_monthly = df_demographic.groupby(df_demographic['date'].dt.to_period('M'))['total_count'].sum()
enrol_monthly = df_enrolment.groupby(df_enrolment['date'].dt.to_period('M'))['total_count'].sum()

x = range(len(bio_monthly))
width = 0.25

ax.bar([i - width for i in x], bio_monthly.values, width, label='Biometric', color=COLORS['biometric'], alpha=0.8)
ax.bar(x, demo_monthly.values[:len(bio_monthly)], width, label='Demographic', color=COLORS['demographic'], alpha=0.8)
ax.bar([i + width for i in x], enrol_monthly.values[:len(bio_monthly)], width, label='Enrolment', color=COLORS['enrolment'], alpha=0.8)

ax.set_xlabel('Month')
ax.set_ylabel('Total Count')
ax.set_title('Monthly Activity Comparison Across All Datasets', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels([str(m) for m in bio_monthly.index], rotation=45)
ax.legend()

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '09_monthly_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 09_monthly_trends.png")

# 10. Top Districts Deep Dive
print("\n📊 Creating Top Districts Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top 20 districts by total activity
all_districts = pd.concat([
    df_biometric.groupby(['state_clean', 'district_clean'])['total_count'].sum().rename('Biometric'),
    df_demographic.groupby(['state_clean', 'district_clean'])['total_count'].sum().rename('Demographic'),
    df_enrolment.groupby(['state_clean', 'district_clean'])['total_count'].sum().rename('Enrolment')
], axis=1).fillna(0)

all_districts['Total'] = all_districts.sum(axis=1)
top_20 = all_districts.nlargest(20, 'Total')

# Stacked bar for top 20 districts
top_20[['Biometric', 'Demographic', 'Enrolment']].plot(kind='barh', stacked=True, ax=axes[0,0],
                                                         color=[COLORS['biometric'], COLORS['demographic'], COLORS['enrolment']])
axes[0,0].set_title('Top 20 Districts - Activity Breakdown', fontweight='bold')
axes[0,0].set_xlabel('Total Count')
axes[0,0].set_ylabel('State - District')
labels = [f"{idx[0][:15]} - {idx[1][:15]}" for idx in top_20.index]
axes[0,0].set_yticklabels(labels, fontsize=8)

# Pincode density
bio_pincode = df_biometric.groupby('pincode')['total_count'].sum().sort_values(ascending=False)
axes[0,1].hist(bio_pincode.values, bins=50, color=COLORS['biometric'], alpha=0.7, edgecolor='black')
axes[0,1].set_title('Pincode Activity Distribution (Biometric)', fontweight='bold')
axes[0,1].set_xlabel('Total Updates per Pincode')
axes[0,1].set_ylabel('Frequency')
axes[0,1].axvline(bio_pincode.mean(), color='red', linestyle='--', label=f'Mean: {bio_pincode.mean():,.0f}')
axes[0,1].legend()

# Scatter: Biometric vs Demographic by State
state_comparison = pd.DataFrame({
    'Biometric': df_biometric.groupby('state_clean')['total_count'].sum(),
    'Demographic': df_demographic.groupby('state_clean')['total_count'].sum()
}).dropna()

axes[1,0].scatter(state_comparison['Biometric'], state_comparison['Demographic'], 
                  alpha=0.7, c=COLORS['primary'], s=100, edgecolor='white')
# Add labels for top 5 states
for state in state_comparison.nlargest(5, 'Biometric').index:
    axes[1,0].annotate(state[:10], (state_comparison.loc[state, 'Biometric'], 
                                     state_comparison.loc[state, 'Demographic']),
                       fontsize=8, alpha=0.8)
axes[1,0].set_xlabel('Biometric Updates')
axes[1,0].set_ylabel('Demographic Updates')
axes[1,0].set_title('State-wise: Biometric vs Demographic Correlation', fontweight='bold')

# Calculate and display correlation
corr = state_comparison['Biometric'].corr(state_comparison['Demographic'])
axes[1,0].text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=axes[1,0].transAxes,
               fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))

# Activity heatmap by weekday and week
bio_pivot = df_biometric.pivot_table(values='total_count', index='weekday', 
                                      columns='week_of_year', aggfunc='sum').fillna(0)
sns.heatmap(bio_pivot, cmap='YlOrRd', ax=axes[1,1], cbar_kws={'label': 'Total Updates'})
axes[1,1].set_title('Biometric Activity Heatmap (Weekday × Week)', fontweight='bold')
axes[1,1].set_xlabel('Week of Year')
axes[1,1].set_ylabel('Day of Week')
axes[1,1].set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '10_bivariate_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 10_bivariate_analysis.png")
