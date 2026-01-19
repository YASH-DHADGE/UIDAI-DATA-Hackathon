# =============================================================================
# 8. TRIVARIATE ANALYSIS
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 7: TRIVARIATE ANALYSIS")
print("=" * 60)

# 11. State × Age × Time Analysis
print("\n📊 Creating Trivariate Visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Get top 5 states
top_5_states = df_enrolment.groupby('state_clean')['total_count'].sum().nlargest(5).index.tolist()

# Age group trends over time for top 5 states
enrol_age_cols = [c for c in df_enrolment.columns if 'age' in c.lower() and c not in ['total_count']]
if enrol_age_cols:
    for state in top_5_states[:3]:
        state_data = df_enrolment[df_enrolment['state_clean'] == state]
        monthly = state_data.groupby(state_data['date'].dt.to_period('M'))[enrol_age_cols].sum()
        monthly.index = monthly.index.astype(str)
        monthly.plot(ax=axes[0,0], marker='o', linewidth=2, alpha=0.7)
    
    axes[0,0].set_title('Top 3 States - Age Group Trends Over Time', fontweight='bold')
    axes[0,0].set_xlabel('Month')
    axes[0,0].set_ylabel('Count')
    axes[0,0].legend(bbox_to_anchor=(1.02, 1), title='Age Group', fontsize=8)
    axes[0,0].tick_params(axis='x', rotation=45)

# 3D-like visualization: Bubble chart (State × Day × Activity)
state_day = df_enrolment.groupby(['state_clean', 'day_name']).agg({
    'total_count': ['sum', 'mean']
}).reset_index()
state_day.columns = ['State', 'Day', 'Total', 'Average']
state_day = state_day[state_day['State'].isin(top_5_states)]

# Encode day as numeric
day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
state_day['Day_Num'] = state_day['Day'].map(day_map)
state_day['State_Num'] = pd.factorize(state_day['State'])[0]

scatter = axes[0,1].scatter(state_day['Day_Num'], state_day['State_Num'], 
                             s=state_day['Total']/state_day['Total'].max()*1000,
                             c=state_day['Average'], cmap='YlOrRd', alpha=0.7, edgecolors='black')
axes[0,1].set_xticks(range(7))
axes[0,1].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
axes[0,1].set_yticks(range(len(top_5_states)))
axes[0,1].set_yticklabels(top_5_states, fontsize=9)
axes[0,1].set_title('State × Day Activity (Bubble Size = Total, Color = Avg)', fontweight='bold')
plt.colorbar(scatter, ax=axes[0,1], label='Average Count')

# Heatmap: State × Month (Biometric activity)
bio_state_month = df_biometric.pivot_table(
    values='total_count', 
    index='state_clean', 
    columns=df_biometric['date'].dt.month,
    aggfunc='sum'
).fillna(0)
# Keep only top 15 states
bio_state_month = bio_state_month.loc[bio_state_month.sum(axis=1).nlargest(15).index]

sns.heatmap(bio_state_month, cmap='Purples', ax=axes[1,0], cbar_kws={'label': 'Total Updates'},
            fmt='.0f', linewidths=0.3)
axes[1,0].set_title('Biometric Updates: State × Month Heatmap', fontweight='bold')
axes[1,0].set_xlabel('Month')
axes[1,0].set_ylabel('State')

# District activity comparison across datasets
# Get top 15 districts overall
top_districts = all_districts.nlargest(15, 'Total')
top_districts['Biometric_pct'] = top_districts['Biometric'] / top_districts['Total'] * 100
top_districts['Demographic_pct'] = top_districts['Demographic'] / top_districts['Total'] * 100
top_districts['Enrolment_pct'] = top_districts['Enrolment'] / top_districts['Total'] * 100

# Stacked percentage bar
top_districts[['Biometric_pct', 'Demographic_pct', 'Enrolment_pct']].plot(
    kind='barh', stacked=True, ax=axes[1,1],
    color=[COLORS['biometric'], COLORS['demographic'], COLORS['enrolment']], alpha=0.85
)
axes[1,1].set_title('Top 15 Districts - Activity Composition (%)', fontweight='bold')
axes[1,1].set_xlabel('Percentage')
axes[1,1].legend(['Biometric', 'Demographic', 'Enrolment'], loc='lower right')
labels = [f"{idx[0][:12]}..." for idx in top_districts.index]
axes[1,1].set_yticklabels(labels, fontsize=8)

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '11_trivariate_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 11_trivariate_analysis.png")

# 12. Geographic Pattern Summary
print("\n📊 Creating Geographic Summary...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# State-wise summary statistics
state_summary = pd.DataFrame({
    'Bio_Total': df_biometric.groupby('state_clean')['total_count'].sum(),
    'Bio_Mean': df_biometric.groupby('state_clean')['total_count'].mean(),
    'Demo_Total': df_demographic.groupby('state_clean')['total_count'].sum(),
    'Demo_Mean': df_demographic.groupby('state_clean')['total_count'].mean(),
    'Enrol_Total': df_enrolment.groupby('state_clean')['total_count'].sum(),
    'Enrol_Mean': df_enrolment.groupby('state_clean')['total_count'].mean(),
}).fillna(0)
state_summary['Grand_Total'] = state_summary['Bio_Total'] + state_summary['Demo_Total'] + state_summary['Enrol_Total']

# Top 15 states by grand total
top_states_summary = state_summary.nlargest(15, 'Grand_Total')

# Multi-bar comparison
x = np.arange(len(top_states_summary))
width = 0.25
axes[0,0].bar(x - width, top_states_summary['Bio_Total']/1e6, width, label='Biometric', color=COLORS['biometric'])
axes[0,0].bar(x, top_states_summary['Demo_Total']/1e6, width, label='Demographic', color=COLORS['demographic'])
axes[0,0].bar(x + width, top_states_summary['Enrol_Total']/1e6, width, label='Enrolment', color=COLORS['enrolment'])
axes[0,0].set_ylabel('Total (Millions)')
axes[0,0].set_title('Top 15 States - Total Activity by Type', fontweight='bold')
axes[0,0].set_xticks(x)
axes[0,0].set_xticklabels([s[:12] for s in top_states_summary.index], rotation=45, ha='right', fontsize=8)
axes[0,0].legend()

# Activity intensity (mean per record)
axes[0,1].scatter(top_states_summary['Bio_Mean'], top_states_summary['Demo_Mean'],
                  s=top_states_summary['Enrol_Mean']*2, alpha=0.7, c=range(len(top_states_summary)),
                  cmap='viridis', edgecolors='black')
for i, state in enumerate(top_states_summary.index[:5]):
    axes[0,1].annotate(state[:10], (top_states_summary.loc[state, 'Bio_Mean'], 
                                     top_states_summary.loc[state, 'Demo_Mean']),
                       fontsize=8)
axes[0,1].set_xlabel('Avg Biometric Updates per Record')
axes[0,1].set_ylabel('Avg Demographic Updates per Record')
axes[0,1].set_title('State Activity Intensity (Bubble=Enrolment Avg)', fontweight='bold')

# Bottom states analysis (lowest activity)
bottom_states = state_summary.nsmallest(10, 'Grand_Total')
bottom_states[['Bio_Total', 'Demo_Total', 'Enrol_Total']].plot(kind='barh', stacked=True, ax=axes[1,0],
    color=[COLORS['biometric'], COLORS['demographic'], COLORS['enrolment']])
axes[1,0].set_title('Bottom 10 States - Activity (Potential Underserved)', fontweight='bold')
axes[1,0].set_xlabel('Total Count')
axes[1,0].legend(['Biometric', 'Demographic', 'Enrolment'])

# Pincode coverage analysis
pincode_counts = pd.DataFrame({
    'Bio_Pincodes': df_biometric.groupby('state_clean')['pincode'].nunique(),
    'Demo_Pincodes': df_demographic.groupby('state_clean')['pincode'].nunique(),
    'Enrol_Pincodes': df_enrolment.groupby('state_clean')['pincode'].nunique()
}).fillna(0)
pincode_top = pincode_counts.loc[top_states_summary.index]

pincode_top.plot(kind='bar', ax=axes[1,1], color=[COLORS['biometric'], COLORS['demographic'], COLORS['enrolment']], alpha=0.8)
axes[1,1].set_title('Pincode Coverage by State', fontweight='bold')
axes[1,1].set_xlabel('State')
axes[1,1].set_ylabel('Unique Pincodes')
axes[1,1].tick_params(axis='x', rotation=45)
axes[1,1].legend(['Biometric', 'Demographic', 'Enrolment'])

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '12_geographic_summary.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 12_geographic_summary.png")
