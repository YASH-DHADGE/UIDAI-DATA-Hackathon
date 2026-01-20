"""
Anomaly Detection and Pattern Analysis for UIDAI Datasets
==========================================================
Analyzes cleaned datasets to identify:
1. High enrolment + low biometric updates (misuse detection)
2. High adult demographics + low child enrolment (data imbalance)
3. Sudden spikes across all datasets (mass registration events)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "cleaned_data"
OUTPUT_DIR = DATA_DIR  # Save outputs in same directory

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def load_cleaned_data():
    """Load all cleaned datasets."""
    print("Loading cleaned datasets...")
    enrolment_df = pd.read_csv(DATA_DIR / "enrolment_cleaned.csv")
    demographic_df = pd.read_csv(DATA_DIR / "demographic_cleaned.csv")
    biometric_df = pd.read_csv(DATA_DIR / "biometric_cleaned.csv")
    
    print(f"  Enrolment:   {enrolment_df.shape[0]:,} rows")
    print(f"  Demographic: {demographic_df.shape[0]:,} rows")
    print(f"  Biometric:   {biometric_df.shape[0]:,} rows")
    
    return enrolment_df, demographic_df, biometric_df


# =============================================================================
# PATTERN 1: High Enrolment + Low Biometric Updates (Misuse Detection)
# =============================================================================

def analyze_misuse_pattern(enrolment_df, biometric_df):
    """
    Detect pincodes with high enrolment but low biometric update rates.
    This may indicate potential misuse or fraud.
    """
    print("\n" + "="*70)
    print("PATTERN 1: Misuse Detection (High Enrolment + Low Biometric)")
    print("="*70)
    
    # Calculate total enrolments per pincode (sum all age groups)
    enrolment_df['total_enrolment'] = (
        enrolment_df['age_0_5'] + 
        enrolment_df['age_5_17'] + 
        enrolment_df['age_18_greater']
    )
    
    # Aggregate by pincode
    enrolment_by_pincode = enrolment_df.groupby('pincode').agg({
        'total_enrolment': 'sum',
        'state': 'first',
        'district': 'first'
    }).reset_index()
    enrolment_by_pincode.columns = ['pincode', 'enrolment_count', 'state', 'district']
    
    # Calculate total biometric updates per pincode
    biometric_df['total_biometric'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']
    
    biometric_by_pincode = biometric_df.groupby('pincode').agg({
        'total_biometric': 'sum'
    }).reset_index()
    biometric_by_pincode.columns = ['pincode', 'biometric_update_count']
    
    # Merge datasets
    merged = enrolment_by_pincode.merge(biometric_by_pincode, on='pincode', how='outer').fillna(0)
    
    # Calculate biometric update rate
    merged['biometric_rate'] = np.where(
        merged['enrolment_count'] > 0,
        (merged['biometric_update_count'] / merged['enrolment_count']) * 100,
        0
    )
    
    # Define thresholds (top 25% enrolment, bottom 25% biometric rate)
    high_enrol_threshold = merged['enrolment_count'].quantile(0.75)
    low_bio_threshold = merged[merged['biometric_rate'] > 0]['biometric_rate'].quantile(0.25)
    
    print(f"\nThresholds:")
    print(f"  High Enrolment (75th percentile): {high_enrol_threshold:,.0f}")
    print(f"  Low Biometric Rate (25th percentile): {low_bio_threshold:.2f}%")
    
    # Identify suspicious pincodes
    suspicious = merged[
        (merged['enrolment_count'] >= high_enrol_threshold) & 
        (merged['biometric_rate'] <= low_bio_threshold) &
        (merged['biometric_rate'] > 0)
    ].sort_values('enrolment_count', ascending=False)
    
    print(f"\nSuspicious Pincodes Found: {len(suspicious)}")
    if len(suspicious) > 0:
        print(f"  Total Enrolments in Suspicious Areas: {suspicious['enrolment_count'].sum():,.0f}")
        print(f"  Avg Biometric Rate in Suspicious Areas: {suspicious['biometric_rate'].mean():.2f}%")
        print("\nTop 10 Suspicious Pincodes:")
        print(suspicious[['pincode', 'state', 'district', 'enrolment_count', 'biometric_rate']].head(10).to_string(index=False))
    
    # Save to CSV
    suspicious.to_csv(OUTPUT_DIR / "suspicious_pincodes_misuse.csv", index=False)
    print(f"\n✓ Saved: suspicious_pincodes_misuse.csv")
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Normal points
    normal = merged[~merged['pincode'].isin(suspicious['pincode'])]
    ax.scatter(normal['enrolment_count'], normal['biometric_rate'], 
               alpha=0.4, s=30, color='#3498db', label='Normal', edgecolors='none')
    
    # Suspicious points
    if len(suspicious) > 0:
        ax.scatter(suspicious['enrolment_count'], suspicious['biometric_rate'], 
                   alpha=0.8, s=100, color='#e74c3c', label='Suspicious (Possible Misuse)', 
                   marker='X', edgecolors='black', linewidths=0.5)
    
    # Threshold lines
    ax.axhline(y=low_bio_threshold, color='#f39c12', linestyle='--', linewidth=2,
               label=f'Low Biometric Threshold ({low_bio_threshold:.1f}%)')
    ax.axvline(x=high_enrol_threshold, color='#27ae60', linestyle='--', linewidth=2,
               label=f'High Enrolment Threshold ({high_enrol_threshold:,.0f})')
    
    ax.set_xlabel('Total Enrolment Count', fontsize=12, fontweight='bold')
    ax.set_ylabel('Biometric Update Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Pattern 1: Misuse Detection\nHigh Enrolment + Low Biometric Updates', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "pattern1_misuse_detection.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: pattern1_misuse_detection.png")
    
    return suspicious, merged, high_enrol_threshold, low_bio_threshold


# =============================================================================
# PATTERN 2: High Adult Demographics + Low Child Enrolment (Data Imbalance)
# =============================================================================

def analyze_imbalance_pattern(enrolment_df, demographic_df):
    """
    Detect pincodes with high adult demographic updates but low child enrolments.
    This indicates potential data collection imbalance.
    """
    print("\n" + "="*70)
    print("PATTERN 2: Data Imbalance (High Adult Demo + Low Child Enrolment)")
    print("="*70)
    
    # Calculate child enrolments (age_0_5 + age_5_17)
    enrolment_df['child_enrolment'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17']
    
    child_by_pincode = enrolment_df.groupby('pincode').agg({
        'child_enrolment': 'sum',
        'state': 'first',
        'district': 'first'
    }).reset_index()
    
    # Calculate adult demographic updates (demo_age_17_ = adults 17+)
    adult_demo_by_pincode = demographic_df.groupby('pincode').agg({
        'demo_age_17_': 'sum'
    }).reset_index()
    adult_demo_by_pincode.columns = ['pincode', 'adult_demographic_count']
    
    # Merge datasets
    imbalance = child_by_pincode.merge(adult_demo_by_pincode, on='pincode', how='outer').fillna(0)
    
    # Calculate adult-to-child ratio
    imbalance['adult_child_ratio'] = np.where(
        imbalance['child_enrolment'] > 0,
        imbalance['adult_demographic_count'] / imbalance['child_enrolment'],
        np.inf
    )
    
    # Handle inf values for display
    imbalance['adult_child_ratio'] = imbalance['adult_child_ratio'].replace([np.inf], np.nan)
    
    # Define thresholds
    high_adult_threshold = imbalance['adult_demographic_count'].quantile(0.75)
    low_child_threshold = imbalance[imbalance['child_enrolment'] > 0]['child_enrolment'].quantile(0.25)
    
    print(f"\nThresholds:")
    print(f"  High Adult Demographics (75th percentile): {high_adult_threshold:,.0f}")
    print(f"  Low Child Enrolment (25th percentile): {low_child_threshold:,.0f}")
    
    # Identify imbalanced pincodes
    imbalanced = imbalance[
        (imbalance['adult_demographic_count'] >= high_adult_threshold) & 
        (imbalance['child_enrolment'] <= low_child_threshold) &
        (imbalance['child_enrolment'] > 0)
    ].sort_values('adult_child_ratio', ascending=False)
    
    print(f"\nImbalanced Pincodes Found: {len(imbalanced)}")
    if len(imbalanced) > 0:
        print(f"  Avg Adult-Child Ratio: {imbalanced['adult_child_ratio'].mean():.2f}")
        print("\nTop 10 Imbalanced Pincodes:")
        print(imbalanced[['pincode', 'state', 'district', 'adult_demographic_count', 
                          'child_enrolment', 'adult_child_ratio']].head(10).to_string(index=False))
    
    # Save to CSV
    imbalanced.to_csv(OUTPUT_DIR / "imbalanced_pincodes.csv", index=False)
    print(f"\n✓ Saved: imbalanced_pincodes.csv")
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Normal points
    normal = imbalance[~imbalance['pincode'].isin(imbalanced['pincode'])]
    ax.scatter(normal['adult_demographic_count'], normal['child_enrolment'], 
               alpha=0.4, s=30, color='#27ae60', label='Normal', edgecolors='none')
    
    # Imbalanced points
    if len(imbalanced) > 0:
        ax.scatter(imbalanced['adult_demographic_count'], imbalanced['child_enrolment'], 
                   alpha=0.8, s=100, color='#e74c3c', label='Imbalanced', 
                   marker='X', edgecolors='black', linewidths=0.5)
    
    # Threshold lines
    ax.axhline(y=low_child_threshold, color='#f39c12', linestyle='--', linewidth=2,
               label=f'Low Child Threshold ({low_child_threshold:,.0f})')
    ax.axvline(x=high_adult_threshold, color='#9b59b6', linestyle='--', linewidth=2,
               label=f'High Adult Threshold ({high_adult_threshold:,.0f})')
    
    ax.set_xlabel('Adult Demographic Updates', fontsize=12, fontweight='bold')
    ax.set_ylabel('Child Enrolment Count', fontsize=12, fontweight='bold')
    ax.set_title('Pattern 2: Data Imbalance\nHigh Adult Demographics + Low Child Enrolment', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "pattern2_data_imbalance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: pattern2_data_imbalance.png")
    
    return imbalanced, imbalance


# =============================================================================
# PATTERN 3: Sudden Spikes Across All Datasets (Mass Registration Events)
# =============================================================================

def analyze_spike_pattern(enrolment_df, demographic_df, biometric_df):
    """
    Detect dates with sudden spikes in activity across all three datasets.
    These may indicate mass registration events.
    """
    print("\n" + "="*70)
    print("PATTERN 3: Mass Registration Events (Sudden Spikes)")
    print("="*70)
    
    # Calculate total activity per date
    enrolment_df['total'] = (enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + 
                             enrolment_df['age_18_greater'])
    demographic_df['total'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']
    biometric_df['total'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']
    
    # Aggregate by date
    enrol_daily = enrolment_df.groupby('date')['total'].sum().reset_index()
    enrol_daily.columns = ['date', 'enrolment_count']
    
    demo_daily = demographic_df.groupby('date')['total'].sum().reset_index()
    demo_daily.columns = ['date', 'demographic_count']
    
    bio_daily = biometric_df.groupby('date')['total'].sum().reset_index()
    bio_daily.columns = ['date', 'biometric_count']
    
    # Convert dates
    enrol_daily['date'] = pd.to_datetime(enrol_daily['date'], format='%d-%m-%Y')
    demo_daily['date'] = pd.to_datetime(demo_daily['date'], format='%d-%m-%Y')
    bio_daily['date'] = pd.to_datetime(bio_daily['date'], format='%d-%m-%Y')
    
    # Sort by date
    enrol_daily = enrol_daily.sort_values('date')
    demo_daily = demo_daily.sort_values('date')
    bio_daily = bio_daily.sort_values('date')
    
    # Calculate z-scores for spike detection
    SPIKE_THRESHOLD = 2.0
    
    enrol_daily['z_score'] = np.abs(stats.zscore(enrol_daily['enrolment_count']))
    demo_daily['z_score'] = np.abs(stats.zscore(demo_daily['demographic_count']))
    bio_daily['z_score'] = np.abs(stats.zscore(bio_daily['biometric_count']))
    
    # Identify spike dates
    enrol_spikes = set(enrol_daily[enrol_daily['z_score'] > SPIKE_THRESHOLD]['date'])
    demo_spikes = set(demo_daily[demo_daily['z_score'] > SPIKE_THRESHOLD]['date'])
    bio_spikes = set(bio_daily[bio_daily['z_score'] > SPIKE_THRESHOLD]['date'])
    
    # Mass registration = spikes in ALL three datasets
    mass_reg_dates = enrol_spikes.intersection(demo_spikes).intersection(bio_spikes)
    
    print(f"\nSpike Detection (z-score > {SPIKE_THRESHOLD}):")
    print(f"  Spike dates in Enrolment:   {len(enrol_spikes)}")
    print(f"  Spike dates in Demographic: {len(demo_spikes)}")
    print(f"  Spike dates in Biometric:   {len(bio_spikes)}")
    print(f"  Mass Registration Events (all 3): {len(mass_reg_dates)}")
    
    # Create detailed report
    mass_reg_report = []
    for date in sorted(mass_reg_dates):
        enrol_count = enrol_daily[enrol_daily['date'] == date]['enrolment_count'].values[0]
        demo_count = demo_daily[demo_daily['date'] == date]['demographic_count'].values[0]
        bio_count = bio_daily[bio_daily['date'] == date]['biometric_count'].values[0]
        
        mass_reg_report.append({
            'date': date.strftime('%Y-%m-%d'),
            'enrolment_count': int(enrol_count),
            'demographic_count': int(demo_count),
            'biometric_count': int(bio_count),
            'total_activity': int(enrol_count + demo_count + bio_count)
        })
    
    mass_reg_df = pd.DataFrame(mass_reg_report).sort_values('total_activity', ascending=False)
    
    if len(mass_reg_df) > 0:
        print(f"\nMass Registration Events:")
        print(mass_reg_df.to_string(index=False))
    
    # Save to CSV
    mass_reg_df.to_csv(OUTPUT_DIR / "mass_registration_events.csv", index=False)
    print(f"\n✓ Saved: mass_registration_events.csv")
    
    # Create visualization
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    
    colors = ['#3498db', '#27ae60', '#f39c12']
    datasets = [
        (enrol_daily, 'enrolment_count', 'Enrolment', enrol_spikes),
        (demo_daily, 'demographic_count', 'Demographic', demo_spikes),
        (bio_daily, 'biometric_count', 'Biometric', bio_spikes)
    ]
    
    for i, (df, col, name, spikes) in enumerate(datasets):
        ax = axes[i]
        ax.plot(df['date'], df[col], color=colors[i], linewidth=1.5, label=f'Daily {name}')
        ax.fill_between(df['date'], df[col], alpha=0.2, color=colors[i])
        
        # Mark mass registration dates
        for date in mass_reg_dates:
            ax.axvline(x=date, color='#e74c3c', linestyle='--', alpha=0.7, linewidth=1.5)
        
        ax.set_ylabel(f'{name} Count', fontsize=11, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(alpha=0.3)
        
        if i == 0:
            ax.set_title('Pattern 3: Mass Registration Events\nSudden Spikes Across All Datasets', 
                        fontsize=14, fontweight='bold', pad=15)
    
    axes[-1].set_xlabel('Date', fontsize=12, fontweight='bold')
    
    # Add legend for mass registration markers
    if len(mass_reg_dates) > 0:
        axes[0].annotate('Red lines = Mass Registration Events', 
                        xy=(0.02, 0.95), xycoords='axes fraction',
                        fontsize=9, color='#e74c3c', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "pattern3_mass_registration_spikes.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: pattern3_mass_registration_spikes.png")
    
    return mass_reg_df, enrol_daily, demo_daily, bio_daily


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("="*70)
    print("ANOMALY DETECTION AND PATTERN ANALYSIS")
    print("="*70)
    
    # Load data
    enrolment_df, demographic_df, biometric_df = load_cleaned_data()
    
    # Pattern 1: Misuse Detection
    suspicious, merged_misuse, high_enrol, low_bio = analyze_misuse_pattern(
        enrolment_df.copy(), biometric_df.copy()
    )
    
    # Pattern 2: Data Imbalance
    imbalanced, merged_imbalance = analyze_imbalance_pattern(
        enrolment_df.copy(), demographic_df.copy()
    )
    
    # Pattern 3: Mass Registration Spikes
    mass_reg, enrol_daily, demo_daily, bio_daily = analyze_spike_pattern(
        enrolment_df.copy(), demographic_df.copy(), biometric_df.copy()
    )
    
    # Final Summary
    print("\n" + "="*70)
    print("ANOMALY DETECTION SUMMARY REPORT")
    print("="*70)
    
    print(f"\n1. MISUSE INDICATORS (High Enrolment + Low Biometric)")
    print(f"   Suspicious Pincodes: {len(suspicious)}")
    if len(suspicious) > 0:
        print(f"   Total Enrolments in Suspicious Areas: {suspicious['enrolment_count'].sum():,.0f}")
        print(f"   Avg Biometric Rate: {suspicious['biometric_rate'].mean():.2f}%")
    
    print(f"\n2. DATA IMBALANCE (High Adult + Low Child)")
    print(f"   Imbalanced Pincodes: {len(imbalanced)}")
    if len(imbalanced) > 0:
        print(f"   Avg Adult-Child Ratio: {imbalanced['adult_child_ratio'].mean():.2f}")
    
    print(f"\n3. MASS REGISTRATION EVENTS")
    print(f"   Mass Registration Dates: {len(mass_reg)}")
    if len(mass_reg) > 0:
        print(f"   Date Range: {mass_reg['date'].min()} to {mass_reg['date'].max()}")
        print(f"   Peak Activity: {mass_reg['total_activity'].max():,}")
    
    print("\n" + "="*70)
    print("OUTPUT FILES (saved to cleaned_data/):")
    print("="*70)
    print("  CSV Reports:")
    print("    - suspicious_pincodes_misuse.csv")
    print("    - imbalanced_pincodes.csv")
    print("    - mass_registration_events.csv")
    print("  Visualizations:")
    print("    - pattern1_misuse_detection.png")
    print("    - pattern2_data_imbalance.png")
    print("    - pattern3_mass_registration_spikes.png")
    print("\n✓ Analysis complete!")
    
    return suspicious, imbalanced, mass_reg


if __name__ == "__main__":
    main()
