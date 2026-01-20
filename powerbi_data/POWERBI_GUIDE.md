# Power BI Data Import Guide - UIDAI Aadhaar Analytics

## Quick Start

### Step 1: Open Power BI Desktop
Launch Power BI Desktop on your computer.

### Step 2: Import Data
1. Click **Home** → **Get Data** → **Text/CSV**
2. Navigate to: `D:\Aadhar data hackathon\UIDAI-DATA-Hackathon\powerbi_data\`
3. Import these files in order:

| File | Purpose | Rows |
|------|---------|------|
| `daily_national_summary.csv` | Daily trends (main fact table) | ~70 |
| `state_summary.csv` | State-level aggregates | ~64 |
| `district_summary.csv` | District-level aggregates | ~1,000+ |
| `state_date_trends.csv` | State trends over time | ~2,500+ |

### Step 3: Create Relationships (Data Model)
In **Model View**, create these relationships:

```
daily_national_summary[date] → state_date_trends[date] (Many-to-Many)
state_summary[state] → state_date_trends[state] (One-to-Many)
state_summary[state] → district_summary[state] (One-to-Many)
```

---

## Recommended Visuals

### Page 1: Executive Dashboard

| Visual | Data | Configuration |
|--------|------|---------------|
| **Card** | Total Biometric | `SUM(daily_national_summary[bio_total])` |
| **Card** | Total Demographic | `SUM(daily_national_summary[demo_total])` |
| **Card** | Total Enrolment | `SUM(daily_national_summary[enrol_total])` |
| **Line Chart** | Daily Trends | X: date, Y: bio_total, demo_total, enrol_total |
| **Pie Chart** | Activity Split | Values: bio_total, demo_total, enrol_total |

### Page 2: Geographic Analysis

| Visual | Data | Configuration |
|--------|------|---------------|
| **Map** | State Activity | Location: state, Size: total_activity |
| **Bar Chart** | Top 10 States | X: state, Y: total_activity, Top N filter |
| **Table** | District Details | Columns: district, biometric_total, enrolment_total, bio_coverage_pct |

### Page 3: Time Analysis

| Visual | Data | Configuration |
|--------|------|---------------|
| **Column Chart** | Weekday vs Weekend | X: day_name, Y: bio_total |
| **Area Chart** | Monthly Trend | X: month_name, Y: total activity |
| **Matrix** | Week Heatmap | Rows: weekday, Columns: week_num, Values: bio_total |

### Page 4: Coverage & Insights

| Visual | Data | Configuration |
|--------|------|---------------|
| **Scatter Chart** | Biometric Coverage | X: enrolment_total, Y: bio_coverage_pct |
| **Bar Chart** | Bottom 10 Coverage | Filter: lowest bio_coverage_pct |
| **Gauge** | Avg Coverage | Value: AVG(bio_coverage_pct), Target: 100 |

---

## DAX Measures (Copy into Power BI)

```dax
// Total Activity
Total Activity = 
    SUM('daily_national_summary'[bio_total]) + 
    SUM('daily_national_summary'[demo_total]) + 
    SUM('daily_national_summary'[enrol_total])

// Biometric Coverage %
Bio Coverage % = 
    DIVIDE(
        SUM('district_summary'[biometric_total]),
        SUM('district_summary'[enrolment_total]),
        0
    ) * 100

// Weekend Activity Premium
Weekend Premium % = 
    VAR WeekendAvg = CALCULATE(
        AVERAGE('daily_national_summary'[bio_total]),
        'daily_national_summary'[is_weekend] = 1
    )
    VAR WeekdayAvg = CALCULATE(
        AVERAGE('daily_national_summary'[bio_total]),
        'daily_national_summary'[is_weekend] = 0
    )
    RETURN DIVIDE(WeekendAvg - WeekdayAvg, WeekdayAvg, 0) * 100

// Child Share %
Child Share % = 
    DIVIDE(
        SUM('district_summary'[child_enrolment]),
        SUM('district_summary'[enrolment_total]),
        0
    ) * 100
```

---

## Additional Insight Files

Import these for anomaly analysis:

| File | Description |
|------|-------------|
| `suspicious_pincodes_misuse.csv` | 2,410 suspicious pincodes |
| `lowest_biometric_coverage_regions.csv` | 30 lowest coverage districts |
| `low_child_penetration_regions.csv` | 84 low child enrolment regions |
| `delayed_biometric_completion_regions.csv` | 130 delayed regions |
| `high_variance_regions.csv` | 924 high variance regions |

---

## Color Theme Suggestion

| Category | Hex Color |
|----------|-----------|
| Biometric | `#7B1FA2` (Purple) |
| Demographic | `#00897B` (Teal) |
| Enrolment | `#D81B60` (Pink) |
| Primary | `#1E88E5` (Blue) |
| Alert | `#E53935` (Red) |
| Success | `#43A047` (Green) |

---

## Tips

1. **Use Slicers**: Add date range and state slicers for interactivity
2. **Bookmarks**: Create bookmarks for different views (Executive, Detailed, Anomaly)
3. **Conditional Formatting**: Highlight low coverage districts in red
4. **Tooltips**: Add custom tooltips showing detailed metrics on hover
5. **Drill-through**: Enable drill from state to district level

---

*Data prepared on: January 20, 2026*
*Team: CoreTech Labs*
