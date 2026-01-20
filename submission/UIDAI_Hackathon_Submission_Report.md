# UIDAI Data Hackathon 2026 - Submission Report

## Aadhaar Data Analytics: Uncovering Patterns for Improved Service Delivery

**Team:** CoreTech Labs  
**Date:** January 2026  

---

# 1. Problem Statement and Approach

## 1.1 Problem Statement

India's Aadhaar program, the world's largest biometric identification system, processes millions of enrolment and update transactions daily across 28 states and 8 union territories. Despite this massive scale, there is limited understanding of:

1. **Geographic Disparities**: Which states/districts have disproportionately high or low Aadhaar activity?
2. **Temporal Patterns**: Are there seasonal, weekly, or daily patterns that could inform resource allocation?
3. **Update Dynamics**: What drives citizens to update biometric vs. demographic information?
4. **Anomaly Detection**: Are there patterns suggesting potential misuse, data imbalance, or mass registration events?

## 1.2 Proposed Approach

Our analytical framework employs a **multi-layered analysis strategy**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA PROCESSING PIPELINE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. DATA SYNCHRONIZATION                                            │
│     └── Load raw chunks → Find common dates/pincodes → Filter       │
│                                                                      │
│  2. ANOMALY DETECTION                                               │
│     ├── Pattern 1: High enrolment + low biometric (fraud)          │
│     ├── Pattern 2: High adult demo + low child (imbalance)         │
│     └── Pattern 3: Simultaneous spikes (mass registration)         │
│                                                                      │
│  3. COMPREHENSIVE ANALYSIS                                          │
│     └── Visualizations, correlations, insights                     │
│                                                                      │
│  OUTPUT: Cleaned data + Anomaly reports + Visualizations           │
└─────────────────────────────────────────────────────────────────────┘
```

### Technical Stack
| Category | Tools |
|----------|-------|
| Data Processing | Python 3.x, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Statistical Analysis | SciPy (Z-score), Pearson Correlation |

---

# 2. Datasets Used

## 2.1 Dataset Overview

| Dataset | Original Records | Cleaned Records | Time Period |
|---------|-----------------|-----------------|-------------|
| **Biometric Updates** | 1,861,108 | 1,430,718 | March 2025+ |
| **Demographic Updates** | 2,071,700 | 1,490,685 | March 2025+ |
| **Enrolments** | 1,006,029 | 880,336 | March 2025+ |
| **TOTAL** | **4,938,837** | **3,801,739** | - |

## 2.2 Data Synchronization

To ensure consistent cross-dataset analysis, we synchronized all three datasets:

| Metric | Value |
|--------|-------|
| Common Dates | 70 |
| Common Pincodes | 19,410+ |
| Data Retention | ~77% of original records |

### Cleaning Summary
| Dataset | Original | Cleaned | Removed | % Removed |
|---------|----------|---------|---------|-----------|
| Enrolment | 1,006,029 | 880,336 | 125,693 | 12.5% |
| Demographic | 2,071,700 | 1,490,685 | 581,015 | 28.0% |
| Biometric | 1,861,108 | 1,430,718 | 430,390 | 23.1% |

---

# 3. Methodology

## 3.1 Data Cleaning Pipeline

```python
# data_cleaning_sync.py workflow
1. Load all CSV chunks from each dataset directory
2. Concatenate into single dataframe per dataset
3. Standardize date and pincode formats
4. Find intersection of dates across all 3 datasets
5. Find intersection of pincodes across all 3 datasets
6. Filter to keep only rows with common dates AND pincodes
7. Save cleaned datasets to cleaned_data/ folder
```

## 3.2 Anomaly Detection Methods

### Pattern 1: Misuse Detection (High Enrolment + Low Biometric)
```python
# Identifies pincodes with suspicious activity ratios
biometric_rate = biometric_updates / enrolments * 100
suspicious = (enrolments >= 75th_percentile) AND (biometric_rate <= 25th_percentile)
```
- **Logic**: High new enrolments but low subsequent biometric updates may indicate fraudulent registrations
- **Results**: 2,410 suspicious pincodes identified

### Pattern 2: Data Imbalance (High Adult + Low Child)
```python
# Identifies pincodes with age-based data collection gaps
imbalanced = (adult_demographics >= 75th_percentile) AND (child_enrolments <= 25th_percentile)
```
- **Logic**: Regions with high adult activity but low child enrolments may have accessibility issues for children
- **Results**: 13 imbalanced pincodes identified

### Pattern 3: Mass Registration Events (Simultaneous Spikes)
```python
# Statistical spike detection using Z-score
z_score = abs(stats.zscore(daily_counts))
spikes = dates where z_score > 2.0 in ALL THREE datasets
```
- **Logic**: Dates with simultaneous spikes across all datasets indicate mass registration drives
- **Results**: 2 mass registration dates identified

---

# 4. Data Analysis and Visualisation

## 4.1 Executive Summary of Findings

| Key Metric | Value | Insight |
|------------|-------|---------|
| **Total Activity** | 110.2 Million | Massive scale of operations |
| **Top State** | Uttar Pradesh | Leads in biometric updates & enrolments |
| **Weekend Effect** | +32.8% | Citizens prefer weekend services |
| **Bio-Demo Correlation** | r = 0.939 | Strong relationship between update types |
| **Suspicious Pincodes** | 2,410 | Potential misuse indicators |
| **Mass Registration Dates** | 2 | Large-scale registration events |
| **Unique Regions** | 1,083 | State-district combinations analyzed |
| **Top 1% Enrolment Threshold** | 27,172 | 99th percentile for high-volume regions |
| **Delayed Biometric Regions** | 130 | Regions with 7+ day completion lag |

## 4.2 Key Findings

### Finding 1: Geographic Concentration
**Top 5 States** account for >60% of all activity:
1. Uttar Pradesh (~16M)
2. Tamil Nadu (~14M)
3. Madhya Pradesh (~11M)
4. Bihar (~10M)
5. Maharashtra (~9M)

### Finding 2: Weekend Demand Surge
| Day Type | Avg Activity | Difference |
|----------|--------------|------------|
| Weekday | 42,350 | Baseline |
| Weekend | 56,236 | **+32.8%** |

**Recommendation**: Expand weekend operating hours in high-demand areas.

### Finding 3: Anomaly Detection Results

| Pattern | Findings | Action Required |
|---------|----------|-----------------|
| Misuse Detection | 2,410 suspicious pincodes | Investigate high-enrolment/low-biometric areas |
| Data Imbalance | 13 imbalanced pincodes | Improve child enrolment accessibility |
| Mass Registration | 2 event dates | Document and verify data quality |

### Finding 4: Age Distribution Patterns
| Age Group | Enrolments | Biometric | Demographic |
|-----------|------------|-----------|-------------|
| 0-5 years | 8% | - | - |
| 5-17 years | 22% | 35% | 38% |
| 18+ years | 70% | 65% | 62% |

### Finding 5: Regional Biometric Coverage Gaps
| Analysis | Regions | Key Finding |
|----------|---------|-------------|
| **Lowest Coverage** | 30 districts | ASSAM - SIVASAGAR at 0% biometric coverage |
| **Top 1% Enrolment** | 11 regions | MAHARASHTRA - THANE leads with 40,611 enrolments |
| **High Variance** | 924 regions | Coefficient of Variation > 1.763 threshold flagged |

**Recommendation**: Prioritize biometric update drives in lowest-coverage districts.

### Finding 6: Child Aadhaar Penetration Analysis
| Metric | Value |
|--------|-------|
| **10th Percentile Threshold** | 93.03% child share |
| **Low Penetration Regions** | 84 districts |
| **Adult-Only Demographic Zones** | 42 regions (top 5%) |

**Recommendation**: Launch targeted child enrolment campaigns in flagged regions.

### Finding 7: Delayed Biometric Completion
| Metric | Value |
|--------|-------|
| **Regions Analyzed** | 200 (cross-correlation analysis) |
| **7+ Day Delay Regions** | 130 (65%) |
| **Maximum Lag Observed** | 30 days |

**Recommendation**: Investigate process bottlenecks in delayed regions.

---

## 4.3 Visualization Gallery

| # | Visualization | Purpose |
|---|---------------|---------|
| 1 | Time Series | Daily activity trends across datasets |
| 2 | State Distribution | Top 15 states by activity type |
| 3 | Day of Week | Weekday vs weekend patterns |
| 4 | Age Distribution | Pie charts by age group |
| 5 | Analysis Grid | Correlation, heatmaps, monthly trends |
| 6 | Anomaly Detection | Z-score based outlier identification |
| 7 | Executive Dashboard | Comprehensive summary |

### Anomaly Detection Visualizations
| Pattern | Visualization |
|---------|---------------|
| Misuse Detection | `pattern1_misuse_detection.png` |
| Data Imbalance | `pattern2_data_imbalance.png` |
| Mass Registration | `pattern3_mass_registration_spikes.png` |

### Key Insights Visualizations (outputs/)
| # | Visualization | Purpose |
|---|---------------|---------|
| 8 | `step2_top_enrolment_bar.png` | Top 20 highest enrolment regions |
| 9 | `step2_enrol_vs_bio_scatter.png` | Enrolment vs biometric coverage |
| 10 | `step3_lowest_bio_coverage_bar.png` | Bottom 30 biometric coverage districts |
| 11 | `step4_daily_timeseries_outliers.png` | National daily trends with outliers |
| 12 | `step4_cv_distribution.png` | Day-to-day variance distribution |
| 13 | `step5_low_child_penetration.png` | Low child penetration regions |
| 14 | `step6_adult_only_scatter.png` | Adult-only demographic zones |
| 15 | `step7_lag_histogram.png` | Biometric completion lag distribution |
| 16 | `step7_delayed_timeseries.png` | Delayed completion time series |

---

## 4.4 Code Files

| File | Description |
|------|-------------|
| `data_cleaning_sync.py` | Data synchronization script |
| `anomaly_detection.py` | Three-pattern anomaly detection |
| `uidai_data_analysis.py` | Key insights analysis with CSV outputs |
| `notebooks/uidai_analysis.py` | Comprehensive analysis with visualizations |
| `requirements.txt` | Python dependencies |

### Output Files
| Directory | Contents |
|-----------|----------|
| `cleaned_data/` | Synchronized CSVs + anomaly reports + pattern visualizations |
| `visualizations/` | 7 analysis charts + KEY_INSIGHTS.txt |
| `outputs/` | 7 CSV result files + 9 PNG plots + summary.md |

### Key Insights CSV Outputs
| File | Records | Description |
|------|---------|-------------|
| `top_1_percent_enrolment_regions.csv` | 11 | Highest enrolment regions |
| `lowest_biometric_coverage_regions.csv` | 30 | Lowest biometric coverage districts |
| `national_high_variance_dates.csv` | 4 | National outlier days |
| `high_variance_regions.csv` | 924 | High day-to-day variance regions |
| `low_child_penetration_regions.csv` | 84 | Low child Aadhaar regions |
| `high_adult_only_demographic_regions.csv` | 42 | Adult-dominant zones |
| `delayed_biometric_completion_regions.csv` | 130 | Delayed completion regions |

---

# 5. Impact & Applicability

## 5.1 Potential Benefits

| Benefit | Description | Stakeholder |
|---------|-------------|-------------|
| **Fraud Prevention** | 2,410 suspicious pincodes for investigation | UIDAI Security |
| **Improved Accessibility** | 84 regions flagged for child enrolment outreach | Rural populations |
| **Resource Planning** | Weekend demand data for staffing | Operations |
| **Coverage Improvement** | 30 districts identified for biometric update drives | Regional offices |
| **Process Optimization** | 130 regions with delayed biometric completion | Operations |
| **Event Detection** | Mass registration monitoring | Data Quality |

## 5.2 Feasibility of Implementation

1. **Immediate**: Investigate suspicious pincodes (2,410 flagged)
2. **Short-term**: Expand weekend operations (+32.8% demand)
3. **Medium-term**: Child enrolment campaigns in 84 low-penetration regions
4. **Medium-term**: Biometric update drives in 30 lowest-coverage districts
5. **Ongoing**: Automated anomaly detection dashboard

---

# 6. Conclusion

This analysis of **4.9+ million Aadhaar records** reveals actionable insights:

1. **Data Synchronization**: 3,801,739 cleaned records with common dates/pincodes across 1,083 regions
2. **Fraud Detection**: 2,410 suspicious pincodes identified for investigation
3. **Coverage Gaps**: 30 districts with lowest biometric coverage, 84 regions with low child penetration
4. **Process Delays**: 130 regions (65%) showing 7+ day lag in biometric completion
5. **Variance Analysis**: 924 high-variance regions and 4 national outlier days identified
6. **Weekend Demand**: +32.8% activity suggests expanded hours needed
7. **Mass Events**: 2 registration event dates detected

These findings demonstrate the power of data-driven governance in managing India's largest identification program, with clear actionable recommendations for improving service delivery and fraud prevention.

---

# 7. References

1. UIDAI Official Data Portal (provided datasets)
2. Python Documentation (pandas, matplotlib, seaborn, scipy)
3. Statistical Methods: Z-score normalization, Pearson correlation

---

**Appendix: Running the Analysis**

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Synchronize data
python data_cleaning_sync.py

# Step 3: Run anomaly detection
python anomaly_detection.py

# Step 4: Generate visualizations
python notebooks/uidai_analysis.py

# Step 5: Run key insights analysis
python uidai_data_analysis.py
# Outputs: 7 CSVs + 9 PNGs + summary.md saved to ./outputs/
```
