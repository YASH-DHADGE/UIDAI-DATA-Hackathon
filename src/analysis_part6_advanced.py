# =============================================================================
# 9. ANOMALY DETECTION & ADVANCED ANALYTICS
# =============================================================================
print("\n" + "=" * 60)
print("SECTION 8: ANOMALY DETECTION & ADVANCED ANALYTICS")
print("=" * 60)

# 13. Z-Score Anomaly Detection
print("\n🔍 Detecting Anomalies using Z-Score...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Daily anomalies for each dataset
def detect_daily_anomalies(df, name, ax, color, threshold=3):
    """Detect daily anomalies using z-score method."""
    daily = df.groupby('date')['total_count'].sum()
    z_scores = np.abs(stats.zscore(daily.values))
    anomalies = daily[z_scores > threshold]
    
    ax.plot(daily.index, daily.values, color=color, alpha=0.7, linewidth=1)
    ax.scatter(anomalies.index, anomalies.values, color='red', s=100, zorder=5, 
               label=f'Anomalies ({len(anomalies)})', marker='o', edgecolors='black')
    ax.axhline(daily.mean(), color='green', linestyle='--', alpha=0.7, label='Mean')
    ax.axhline(daily.mean() + threshold * daily.std(), color='orange', linestyle=':', alpha=0.7, label=f'+{threshold}σ')
    ax.axhline(daily.mean() - threshold * daily.std(), color='orange', linestyle=':', alpha=0.7)
    ax.set_title(f'{name} - Daily Anomalies (Z > {threshold})', fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Count')
    ax.legend(loc='upper right', fontsize=8)
    
    return anomalies

bio_anomalies = detect_daily_anomalies(df_biometric, 'Biometric', axes[0,0], COLORS['biometric'])
demo_anomalies = detect_daily_anomalies(df_demographic, 'Demographic', axes[0,1], COLORS['demographic'])
enrol_anomalies = detect_daily_anomalies(df_enrolment, 'Enrolment', axes[1,0], COLORS['enrolment'])

# State-level anomaly detection
state_totals = df_biometric.groupby('state_clean')['total_count'].sum()
state_z = np.abs(stats.zscore(state_totals.values))
state_anomalies = state_totals[state_z > 2]

colors = ['red' if z > 2 else COLORS['biometric'] for z in state_z]
axes[1,1].barh(state_totals.sort_values().index, state_totals.sort_values().values, color=colors, alpha=0.7)
axes[1,1].set_title('State-Level Activity (Red = Anomalous)', fontweight='bold')
axes[1,1].set_xlabel('Total Biometric Updates')

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '13_anomaly_detection.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 13_anomaly_detection.png")

# Print anomaly summary
print(f"\n📊 Anomaly Summary (Z-Score > 3):")
print(f"  Biometric: {len(bio_anomalies)} anomalous days detected")
print(f"  Demographic: {len(demo_anomalies)} anomalous days detected")
print(f"  Enrolment: {len(enrol_anomalies)} anomalous days detected")

# 14. Rolling Statistics & Trends
print("\n📊 Creating Rolling Statistics Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# 7-day rolling average
for idx, (name, df, color) in enumerate([
    ('Biometric', df_biometric, COLORS['biometric']),
    ('Demographic', df_demographic, COLORS['demographic']),
]):
    daily = df.groupby('date')['total_count'].sum()
    rolling_7 = daily.rolling(window=7, min_periods=1).mean()
    rolling_30 = daily.rolling(window=30, min_periods=1).mean()
    
    ax = axes[0, idx]
    ax.plot(daily.index, daily.values, alpha=0.3, color=color, label='Daily')
    ax.plot(rolling_7.index, rolling_7.values, color=color, linewidth=2, label='7-day MA')
    ax.plot(rolling_30.index, rolling_30.values, color='red', linewidth=2, linestyle='--', label='30-day MA')
    ax.set_title(f'{name} - Rolling Averages', fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.legend()

# Week-over-week growth rate
weekly_bio = df_biometric.groupby('week_of_year')['total_count'].sum()
weekly_growth = weekly_bio.pct_change() * 100

axes[1,0].bar(weekly_growth.index, weekly_growth.values, 
              color=[COLORS['secondary'] if x >= 0 else COLORS['accent'] for x in weekly_growth.values])
axes[1,0].axhline(0, color='black', linewidth=0.5)
axes[1,0].set_title('Biometric - Week-over-Week Growth Rate (%)', fontweight='bold')
axes[1,0].set_xlabel('Week of Year')
axes[1,0].set_ylabel('Growth Rate (%)')

# Cumulative activity
bio_cum = df_biometric.groupby('date')['total_count'].sum().cumsum()
demo_cum = df_demographic.groupby('date')['total_count'].sum().cumsum()
enrol_cum = df_enrolment.groupby('date')['total_count'].sum().cumsum()

axes[1,1].plot(bio_cum.index, bio_cum.values/1e6, label='Biometric', color=COLORS['biometric'], linewidth=2)
axes[1,1].plot(demo_cum.index, demo_cum.values/1e6, label='Demographic', color=COLORS['demographic'], linewidth=2)
axes[1,1].plot(enrol_cum.index, enrol_cum.values/1e6, label='Enrolment', color=COLORS['enrolment'], linewidth=2)
axes[1,1].set_title('Cumulative Activity Over Time', fontweight='bold')
axes[1,1].set_xlabel('Date')
axes[1,1].set_ylabel('Cumulative Count (Millions)')
axes[1,1].legend()

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '14_rolling_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 14_rolling_trends.png")

# 15. Predictive Insights (Simple Forecasting)
print("\n📊 Creating Forecasting Visualization...")

from scipy.stats import linregress

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (name, df, color) in enumerate([
    ('Biometric', df_biometric, COLORS['biometric']),
    ('Demographic', df_demographic, COLORS['demographic']),
    ('Enrolment', df_enrolment, COLORS['enrolment'])
]):
    daily = df.groupby('date')['total_count'].sum().reset_index()
    daily['day_num'] = (daily['date'] - daily['date'].min()).dt.days
    
    # Linear regression for trend
    slope, intercept, r_value, p_value, std_err = linregress(daily['day_num'], daily['total_count'])
    trend_line = slope * daily['day_num'] + intercept
    
    axes[idx].scatter(daily['date'], daily['total_count'], alpha=0.5, s=20, color=color)
    axes[idx].plot(daily['date'], trend_line, color='red', linewidth=2, linestyle='--', 
                   label=f'Trend (R²={r_value**2:.3f})')
    axes[idx].set_title(f'{name} - Linear Trend', fontweight='bold')
    axes[idx].set_xlabel('Date')
    axes[idx].set_ylabel('Daily Total')
    axes[idx].legend()
    
    # Add trend annotation
    trend_dir = 'Increasing' if slope > 0 else 'Decreasing'
    axes[idx].text(0.05, 0.95, f'{trend_dir}\n{slope:+.1f}/day', transform=axes[idx].transAxes,
                   fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))

plt.tight_layout()
plt.savefig(VISUALIZATIONS_DIR / '15_forecasting.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: 15_forecasting.png")
