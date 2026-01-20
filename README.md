# 🔐 UIDAI Data Hackathon 2026 - Aadhaar Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Team-CoreTech%20Labs-red.svg" alt="Team">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-2.0+-green.svg" alt="Pandas">
  <img src="https://img.shields.io/badge/Hackathon-UIDAI%202026-orange.svg" alt="Hackathon">
  <img src="https://img.shields.io/badge/Records-4.9M+-purple.svg" alt="Records">
</p>

> **Comprehensive analytics solution for analyzing anonymized Aadhaar enrolment and update datasets to uncover meaningful patterns, trends, and anomalies that support UIDAI decision-making.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Findings](#-key-findings)
- [Datasets](#-datasets)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Analysis Pipeline](#-analysis-pipeline)
- [Visualizations](#-visualizations)
- [Technical Stack](#-technical-stack)

---

## 🎯 Overview

This project provides a multi-layered analytical framework for UIDAI's Aadhaar data, processing **4.9+ million records** across three major datasets to deliver actionable insights for service optimization.

### Key Features
- 🧹 **Data Synchronization**: Cleans and aligns datasets by common dates & pincodes
- 🔍 **Anomaly Detection**: Identifies misuse patterns, data imbalances, and mass registration events
- 📊 **Comprehensive Visualizations**: 10+ charts including executive dashboards
- 📈 **Statistical Analysis**: Correlation, z-score anomalies, trend analysis

### Research Questions Addressed
- 📍 Which states/districts have disproportionately high or low Aadhaar activity?
- 📅 Are there seasonal, weekly, or daily patterns for resource allocation?
- 🔄 What drives citizens to update biometric vs. demographic information?
- ⚠️ Are there anomalous patterns indicating potential misuse or data issues?

---

## 🏆 Key Findings

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Activity** | 110.2 Million | Massive scale of operations |
| **Top State** | Uttar Pradesh | Leads in both biometric updates and enrolments |
| **Weekend Effect** | +32.8% | Citizens prefer weekend services |
| **Bio-Demo Correlation** | r = 0.939 | Very strong relationship between update types |
| **States Covered** | 36 | Full national coverage |
| **Synchronized Pincodes** | 19,410+ | Common across all 3 datasets |

### 🚨 Anomaly Detection Results

| Pattern | Description | Findings |
|---------|-------------|----------|
| **Misuse Detection** | High enrolment + low biometric rate | 2,410 suspicious pincodes |
| **Data Imbalance** | High adult demo + low child enrolment | 13 imbalanced pincodes |
| **Mass Registration** | Simultaneous spikes across datasets | 2 mass registration dates |

### 💡 Actionable Recommendations
1. **Geographic Focus**: Prioritize UP, Tamil Nadu, MP, Bihar, Maharashtra
2. **Temporal Optimization**: Expand weekend operations (+32.8% demand)
3. **Bundled Services**: Strong bio-demo correlation supports combined updates
4. **Age-Specific Outreach**: School-based campaigns for child biometric updates
5. **Fraud Prevention**: Investigate 2,410 suspicious high-enrolment/low-biometric pincodes
6. **Biometric Coverage**: Target 30 lowest-coverage districts for update drives
7. **Delay Reduction**: Address 130 regions with 7+ day biometric completion lag

---

## 📊 Datasets

| Dataset | Original Records | Cleaned Records | Description |
|---------|-----------------|-----------------|-------------|
| **Biometric Updates** | 1,861,108 | 1,430,718 | Biometric update records with age distribution |
| **Demographic Updates** | 2,071,700 | 1,490,685 | Demographic update records with age distribution |
| **Enrolments** | 1,006,029 | 880,336 | New Aadhaar enrolment records |
| **TOTAL** | **4,938,837** | **3,801,739** | March-May 2025 |

### Data Synchronization
Datasets are synchronized to retain only:
- **70 common dates** across all three datasets
- **19,410+ common pincodes** across all three datasets

---

## 📁 Project Structure

```
UIDAI-DATA-Hackathon/
│
├── 📂 api_data_aadhar_biometric/     # Raw biometric update data (chunked)
├── 📂 api_data_aadhar_demographic/   # Raw demographic update data (chunked)
├── 📂 api_data_aadhar_enrolment/     # Raw enrolment data (chunked)
│
├── 📂 cleaned_data/                   # ✨ Synchronized & Cleaned Datasets
│   ├── enrolment_cleaned.csv         # Cleaned enrolment (880K rows)
│   ├── demographic_cleaned.csv       # Cleaned demographic (1.49M rows)
│   ├── biometric_cleaned.csv         # Cleaned biometric (1.43M rows)
│   ├── cleaning_summary.csv          # Cleaning statistics
│   ├── suspicious_pincodes_misuse.csv    # Pattern 1 results
│   ├── imbalanced_pincodes.csv           # Pattern 2 results
│   ├── mass_registration_events.csv      # Pattern 3 results
│   └── pattern*.png                      # Anomaly visualizations
│
├── 📂 notebooks/
│   ├── uidai_analysis.ipynb          # Jupyter notebook (original)
│   └── uidai_analysis.py             # Python script (uses cleaned data)
│
├── 📂 visualizations/                 # Generated charts & insights
│   ├── 01_time_series.png            # Daily activity trends
│   ├── 02_states.png                 # Top 15 states by activity
│   ├── 03_weekday.png                # Weekday vs weekend patterns
│   ├── 04_age_dist.png               # Age distribution pie charts
│   ├── 05_analysis_grid.png          # Correlation heatmaps
│   ├── 06_anomalies.png              # Anomaly detection
│   ├── 07_dashboard.png              # Executive dashboard
│   └── KEY_INSIGHTS.txt              # Summary of key findings
│
├── 📂 submission/
│   └── UIDAI_Hackathon_Submission_Report.md  # Final submission report
│
├── 📂 outputs/                        # ✨ Key Insights Analysis Outputs
│   ├── top_1_percent_enrolment_regions.csv
│   ├── lowest_biometric_coverage_regions.csv
│   ├── national_high_variance_dates.csv
│   ├── high_variance_regions.csv
│   ├── low_child_penetration_regions.csv
│   ├── high_adult_only_demographic_regions.csv
│   ├── delayed_biometric_completion_regions.csv
│   ├── step2-7*.png                   # 9 visualization plots
│   └── summary.md                     # Analysis summary report
│
├── data_cleaning_sync.py             # 🧹 Data synchronization script
├── anomaly_detection.py              # 🔍 Anomaly detection script
├── uidai_data_analysis.py            # 📊 Key insights analysis script
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/UIDAI-DATA-Hackathon.git
cd UIDAI-DATA-Hackathon

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Step 1: Data Cleaning & Synchronization
Synchronize datasets to retain only common dates and pincodes:

```bash
python data_cleaning_sync.py
```

**Output**: Cleaned CSVs in `cleaned_data/` folder

### Step 2: Anomaly Detection
Detect misuse patterns, data imbalances, and mass registration events:

```bash
python anomaly_detection.py
```

**Output**: 3 CSV reports + 3 PNG visualizations in `cleaned_data/`

### Step 3: Full Analysis
Run comprehensive analysis with visualizations:

```bash
python notebooks/uidai_analysis.py
```

**Output**: 7 charts + insights in `visualizations/` folder

### Step 4: Key Insights Analysis (NEW)
Generate 6 key insights with CSV outputs and visualizations:

```bash
python uidai_data_analysis.py
```

**Output**: 7 CSVs + 9 PNGs + summary.md in `outputs/` folder

---

## 🔬 Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA PROCESSING PIPELINE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. DATA SYNCHRONIZATION (data_cleaning_sync.py)                    │
│     └── Load raw chunks → Find common dates/pincodes → Filter       │
│                                                                      │
│  2. ANOMALY DETECTION (anomaly_detection.py)                        │
│     ├── Pattern 1: High enrolment + low biometric (fraud)          │
│     ├── Pattern 2: High adult demo + low child (imbalance)         │
│     └── Pattern 3: Simultaneous spikes (mass registration)         │
│                                                                      │
│  3. COMPREHENSIVE ANALYSIS (uidai_analysis.py)                      │
│     ├── Time series analysis                                        │
│     ├── State-wise distribution                                     │
│     ├── Age group analysis                                          │
│     ├── Correlation analysis                                        │
│     └── Executive dashboard                                         │
│                                                                      │
│  4. KEY INSIGHTS ANALYSIS (uidai_data_analysis.py)                  │
│     ├── Top 1% enrolment regions                                    │
│     ├── Lowest biometric coverage districts                         │
│     ├── High variance day-to-day analysis                           │
│     ├── Low child Aadhaar penetration                               │
│     ├── Adult-only demographic zones                                │
│     └── Delayed biometric completion (lag analysis)                 │
│                                                                      │
│  OUTPUT: cleaned_data/ + visualizations/ + outputs/ + insights      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📈 Visualizations

| # | Chart | File | Description |
|---|-------|------|-------------|
| 1 | Time Series | `01_time_series.png` | Daily activity trends |
| 2 | State Distribution | `02_states.png` | Top 15 states by activity |
| 3 | Day of Week | `03_weekday.png` | Weekday vs weekend patterns |
| 4 | Age Distribution | `04_age_dist.png` | Pie charts by age group |
| 5 | Analysis Grid | `05_analysis_grid.png` | Correlation & heatmaps |
| 6 | Anomaly Detection | `06_anomalies.png` | Z-score outliers |
| 7 | Executive Dashboard | `07_dashboard.png` | Summary for decision-makers |

### Anomaly Detection Visualizations (in `cleaned_data/`)
| Pattern | File | Description |
|---------|------|-------------|
| Misuse Detection | `pattern1_misuse_detection.png` | Enrolment vs biometric rate scatter |
| Data Imbalance | `pattern2_data_imbalance.png` | Adult demo vs child enrolment |
| Mass Registration | `pattern3_mass_registration_spikes.png` | Time series with spike markers |

### Key Insights Visualizations (in `outputs/`)
| # | File | Description |
|---|------|-------------|
| 1 | `step2_top_enrolment_bar.png` | Top 20 highest enrolment regions |
| 2 | `step2_enrol_vs_bio_scatter.png` | Enrolment vs biometric coverage |
| 3 | `step3_lowest_bio_coverage_bar.png` | Bottom 30 biometric coverage |
| 4 | `step4_daily_timeseries_outliers.png` | National trends with outliers |
| 5 | `step4_cv_distribution.png` | Day-to-day variance distribution |
| 6 | `step5_low_child_penetration.png` | Low child penetration regions |
| 7 | `step6_adult_only_scatter.png` | Adult-only demographic zones |
| 8 | `step7_lag_histogram.png` | Biometric lag distribution |
| 9 | `step7_delayed_timeseries.png` | Delayed completion time series |

---

## 🛠 Technical Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.9+ |
| **Data Processing** | Pandas, NumPy, SciPy |
| **Visualization** | Matplotlib, Seaborn |
| **Statistical Analysis** | Z-score anomaly detection, Pearson correlation |

---

## ✨ Code Quality

- **PEP 8** compliant styling
- Comprehensive comments and docstrings
- **Reproducible** with fixed random seed (42)
- Error handling for file encoding issues
- Modular, reusable scripts
- Data synchronization for cross-dataset analysis

---

## 📅 Timeline

| Milestone | Status |
|-----------|--------|
<<<<<<< Updated upstream
| Data Collection | ✅ Complete |
| Data Preprocessing | ✅ Complete |
| Exploratory Analysis | ✅ Complete |
| Visualization Generation | ✅ Complete |
| Insights Compilation | ✅ Complete |
=======
| Data Collection | Complete |
| Data Synchronization | Complete |
| Anomaly Detection | Complete |
| Visualization Generation | Complete |
| Insights Compilation | Complete |
| Key Insights Analysis | Complete |
>>>>>>> Stashed changes

---

## 📜 License

This project is developed for the **UIDAI Data Hackathon 2026** by **CoreTech Labs**.

---

<p align="center">
  Made with ❤️ for India's Digital Identity Infrastructure
</p>
