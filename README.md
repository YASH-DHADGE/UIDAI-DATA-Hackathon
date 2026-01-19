# 🔐 UIDAI Data Hackathon 2026 - Aadhaar Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-2.0+-green.svg" alt="Pandas">
  <img src="https://img.shields.io/badge/Hackathon-UIDAI%202026-orange.svg" alt="Hackathon">
  <img src="https://img.shields.io/badge/Records-4.9M+-purple.svg" alt="Records">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
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
- [Analysis Modules](#-analysis-modules)
- [Visualizations](#-visualizations)
- [Technical Stack](#-technical-stack)
- [Contributing](#-contributing)

---

## 🎯 Overview

This project provides a multi-layered analytical framework for UIDAI's Aadhaar data, processing **4.9+ million records** across three major datasets to deliver actionable insights for service optimization.

### Research Questions Addressed
- 📍 Which states/districts have disproportionately high or low Aadhaar activity?
- 📅 Are there seasonal, weekly, or daily patterns for resource allocation?
- 🔄 What drives citizens to update biometric vs. demographic information?
- ⚡ How can UIDAI improve operational efficiency based on data-driven insights?

---

## 🏆 Key Findings

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Activity** | 110.2 Million | Massive scale of operations |
| **Top State** | Uttar Pradesh | Leads in both biometric updates and enrolments |
| **Weekend Effect** | +32.8% | Citizens prefer weekend services |
| **Bio-Demo Correlation** | r = 0.939 | Very strong relationship between update types |
| **States Covered** | 36 | Full national coverage |
| **Unique Pincodes** | 19,000+ | Granular geographic reach |

### 💡 Actionable Recommendations
1. **Geographic Focus**: Prioritize UP, Tamil Nadu, MP, Bihar, Maharashtra
2. **Temporal Optimization**: Expand weekend operations (+32.8% demand)
3. **Bundled Services**: Strong bio-demo correlation supports combined updates
4. **Age-Specific Outreach**: School-based campaigns for child biometric updates
5. **Proactive Monitoring**: Implement anomaly detection for data quality

---

## 📊 Datasets

| Dataset | Records | Size | Description |
|---------|---------|------|-------------|
| **Biometric Updates** | ~1.86M | ~150 MB | Biometric update records with age distribution |
| **Demographic Updates** | ~2.07M | ~170 MB | Demographic update records with age distribution |
| **Enrolments** | ~1.0M | ~85 MB | New Aadhaar enrolment records |
| **TOTAL** | **~4.94M** | **~405 MB** | March 2025 onwards |

### Dataset Schema

<details>
<summary>📁 Biometric Update Dataset</summary>

| Column | Type | Description |
|--------|------|-------------|
| `date` | Date | Date of update (DD-MM-YYYY) |
| `state` | String | Indian state/UT name |
| `district` | String | District within state |
| `pincode` | Integer | 6-digit postal code |
| `bio_age_5_17` | Integer | Biometric updates for age 5-17 |
| `bio_age_17_` | Integer | Biometric updates for age 17+ |
</details>

<details>
<summary>📁 Demographic Update Dataset</summary>

| Column | Type | Description |
|--------|------|-------------|
| `date` | Date | Date of update |
| `state` | String | State name |
| `district` | String | District name |
| `pincode` | Integer | Postal code |
| `demo_age_5_17` | Integer | Demographic updates for age 5-17 |
| `demo_age_17_` | Integer | Demographic updates for age 17+ |
</details>

<details>
<summary>📁 Enrolment Dataset</summary>

| Column | Type | Description |
|--------|------|-------------|
| `date` | Date | Enrolment date |
| `state` | String | State name |
| `district` | String | District name |
| `pincode` | Integer | Postal code |
| `age_0_5` | Integer | Enrolments for age 0-5 |
| `age_5_17` | Integer | Enrolments for age 5-17 |
| `age_18_greater` | Integer | Enrolments for age 18+ |
</details>

---

## 📁 Project Structure

```
uidai-hackathon-2026/
│
├── 📂 api_data_aadhar_biometric/     # Biometric update raw data
├── 📂 api_data_aadhar_demographic/   # Demographic update raw data
├── 📂 api_data_aadhar_enrolment/     # Enrolment raw data
│
├── 📂 notebooks/
│   ├── uidai_analysis.ipynb          # Complete Jupyter notebook
│   └── uidai_analysis.py             # Python source code
│
├── 📂 src/                            # Modular analysis components
│   ├── analysis_part1_loading.py     # Data loading utilities
│   ├── analysis_part2_preprocessing.py  # Data cleaning & preprocessing
│   ├── analysis_part3_visualizations.py  # Basic visualizations
│   ├── analysis_part4_bivariate.py   # Bivariate analysis
│   ├── analysis_part5_trivariate.py  # Trivariate analysis
│   ├── analysis_part6_advanced.py    # Advanced analytics
│   ├── analysis_part7_insights.py    # Insights & recommendations
│   └── complete_analysis.py          # Main runner script
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
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Jupyter Notebook (optional, for interactive analysis)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/uidai-hackathon-2026.git
   cd uidai-hackathon-2026
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import pandas; import matplotlib; print('✅ All dependencies installed!')"
   ```

---

## 💻 Usage

### Option 1: Run Complete Analysis Script
Run all analysis modules in sequence:

```bash
cd "d:\Aadhar data hackathon"
python src/complete_analysis.py
```

This will:
- Load and preprocess all datasets
- Generate 16+ visualizations
- Save insights to `visualizations/KEY_INSIGHTS.txt`
- Create comprehensive charts in `visualizations/` folder

### Option 2: Interactive Jupyter Notebook
For step-by-step exploration:

```bash
jupyter notebook notebooks/uidai_analysis.ipynb
```

### Option 3: Run Individual Modules
For targeted analysis:

```bash
# Data loading only
python src/analysis_part1_loading.py

# Preprocessing
python src/analysis_part2_preprocessing.py

# Generate visualizations
python src/analysis_part3_visualizations.py

# Advanced analytics
python src/analysis_part6_advanced.py
```

---

## 🔬 Analysis Modules

| Module | File | Description |
|--------|------|-------------|
| **Data Loading** | `analysis_part1_loading.py` | CSV parsing with UTF-8-SIG encoding, error handling |
| **Preprocessing** | `analysis_part2_preprocessing.py` | Date parsing, feature engineering, data cleaning |
| **Visualizations** | `analysis_part3_visualizations.py` | Time series, distributions, basic charts |
| **Bivariate** | `analysis_part4_bivariate.py` | Correlations, cross-tabs, comparative analysis |
| **Trivariate** | `analysis_part5_trivariate.py` | Heatmaps, bubble charts, multi-dimensional analysis |
| **Advanced** | `analysis_part6_advanced.py` | Anomaly detection (Z-score), trend analysis, forecasting |
| **Insights** | `analysis_part7_insights.py` | Key findings compilation, recommendations |

### Analytical Methods Used
- **Univariate**: Descriptive statistics, distributions, outlier detection
- **Bivariate**: Pearson correlation, cross-tabulation, weekday/weekend comparison
- **Trivariate**: State × Month × Activity heatmaps, bubble charts
- **Advanced**: Z-score anomaly detection (threshold = 2.5), rolling averages, linear regression

---

## 📈 Visualizations

| # | Chart | Purpose | File |
|---|-------|---------|------|
| 1 | Time Series | Daily activity trends across datasets | `01_time_series.png` |
| 2 | State Distribution | Top 15 states by activity type | `02_states.png` |
| 3 | Day of Week | Weekday vs weekend patterns | `03_weekday.png` |
| 4 | Age Distribution | Pie charts by age group | `04_age_dist.png` |
| 5 | Analysis Grid | Correlation, heatmaps, monthly trends | `05_analysis_grid.png` |
| 6 | Anomaly Detection | Z-score based outlier identification | `06_anomalies.png` |
| 7 | Executive Dashboard | Comprehensive summary for decision-makers | `07_dashboard.png` |

<details>
<summary>📊 Sample Visualization Preview</summary>

The dashboard (`07_dashboard.png`) provides a comprehensive view of:
- Geographic distribution of Aadhaar activity
- Temporal patterns (weekly/monthly)
- Age group breakdowns
- Key performance metrics
</details>

---

## 🛠 Technical Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.9+ |
| **Data Processing** | Pandas ≥2.0.0, NumPy ≥1.24.0, SciPy ≥1.10.0 |
| **Visualization** | Matplotlib ≥3.7.0, Seaborn ≥0.12.0, Plotly ≥5.14.0 |
| **Statistical Analysis** | Statsmodels ≥0.14.0, Scikit-learn ≥1.2.0 |
| **Environment** | Jupyter ≥1.0.0, ipykernel ≥6.22.0 |
| **Export** | nbconvert ≥7.0.0 |

---

## ✨ Code Quality

- ✅ **PEP 8** compliant styling
- ✅ Comprehensive comments and docstrings
- ✅ **Reproducible** with fixed random seed (42)
- ✅ Error handling for file encoding issues
- ✅ Modular, reusable functions
- ✅ Clean separation of concerns

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📅 Timeline

| Milestone | Status |
|-----------|--------|
| Data Collection | ✅ Complete |
| Data Preprocessing | ✅ Complete |
| Exploratory Analysis | ✅ Complete |
| Visualization Generation | ✅ Complete |
| Insights Compilation | ✅ Complete |
| **Submission Deadline** | **January 20, 2026, 11:59 PM** |

---

## 📜 License

This project is developed for the **UIDAI Data Hackathon 2026**. All rights reserved.

---

## 👥 Team

**UIDAI Data Hackathon 2026 Participant**

---

<p align="center">
  Made with ❤️ for India's Digital Identity Infrastructure
</p>
