import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- CONFIGURATION & THEME ---
# Setting the color theme based on POWERBI_GUIDE.md
COLORS = {
    'bio': '#7B1FA2',   # Purple
    'demo': '#00897B',  # Teal
    'enrol': '#D81B60', # Pink
    'primary': '#1E88E5',
    'alert': '#E53935',
    'success': '#43A047'
}

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette([COLORS['bio'], COLORS['demo'], COLORS['enrol']])

# --- DATA LOADING (Using the data provided in the prompt) ---

# 1. Daily National Summary
daily_data = """date,bio_total,demo_total,enrol_total,child_count,adult_count,year,month,month_name,day,weekday,day_name,is_weekend,week_num
2025-04-01,8641630,1515672,257438,232525,24913,2025,4,April,1,1,Tuesday,0,14
2025-05-01,7879908,1566287,183616,167032,16584,2025,5,May,1,3,Thursday,0,18
2025-06-01,7899289,1685562,215734,198854,16880,2025,6,June,1,6,Sunday,1,22
2025-07-01,9792552,2220715,616868,581685,35183,2025,7,July,1,1,Tuesday,0,27
2025-09-01,336402,434285,74989,73912,1077,2025,9,September,1,0,Monday,0,36
2025-09-02,317645,435250,76490,75546,944,2025,9,September,2,1,Tuesday,0,36
2025-09-03,313571,314702,71987,71144,843,2025,9,September,3,2,Wednesday,0,36
2025-09-04,300981,383691,65348,64520,828,2025,9,September,4,3,Thursday,0,36
2025-09-05,95771,273929,26069,25638,431,2025,9,September,5,4,Friday,0,36
2025-09-06,254452,368217,58957,58402,555,2025,9,September,6,5,Saturday,1,36
2025-09-07,32956,89024,14658,14502,156,2025,9,September,7,6,Sunday,1,36
2025-09-08,415658,535581,83351,82474,877,2025,9,September,8,0,Monday,0,37
2025-09-09,413111,508585,88503,87650,853,2025,9,September,9,1,Tuesday,0,37
2025-09-10,388115,483117,84299,83476,823,2025,9,September,10,2,Wednesday,0,37
2025-09-11,412565,377623,73204,72412,792,2025,9,September,11,3,Thursday,0,37
2025-09-12,432620,438808,78857,78062,795,2025,9,September,12,4,Friday,0,37
2025-09-13,307058,318607,56228,55854,374,2025,9,September,13,5,Saturday,1,37
2025-09-14,51405,94966,14990,14849,141,2025,9,September,14,6,Sunday,1,37
2025-09-15,453175,405764,53240,52693,547,2025,9,September,15,0,Monday,0,38
2025-09-16,461025,372495,63846,63114,732,2025,9,September,16,1,Tuesday,0,38
2025-09-17,398511,348132,57408,56826,582,2025,9,September,17,2,Wednesday,0,38
2025-09-18,451780,435045,60598,60089,509,2025,9,September,18,3,Thursday,0,38
2025-09-19,427998,362719,57356,56769,587,2025,9,September,19,4,Friday,0,38
2025-09-20,389397,342888,49376,49119,257,2025,9,September,20,5,Saturday,1,38
2025-10-13,3377,204795,74829,72945,1884,2025,10,October,13,0,Monday,0,42
2025-10-15,295751,462540,58895,57291,1604,2025,10,October,15,2,Wednesday,0,42
2025-10-16,274832,493799,36980,35378,1602,2025,10,October,16,3,Thursday,0,42
2025-10-17,333017,323126,115876,114717,1159,2025,10,October,17,4,Friday,0,42
2025-10-18,356678,173214,56021,55268,753,2025,10,October,18,5,Saturday,1,42
2025-10-19,345387,233330,58972,58622,350,2025,10,October,19,6,Sunday,1,42
2025-10-20,37353,112008,15405,15198,207,2025,10,October,20,0,Monday,0,43
2025-10-21,33400,57384,7643,7282,361,2025,10,October,21,1,Tuesday,0,43
2025-10-22,1681,10448,233,177,56,2025,10,October,22,2,Wednesday,0,43
2025-10-23,9751,25155,1145,263,882,2025,10,October,23,3,Thursday,0,43
2025-10-24,269146,427431,36205,35195,1010,2025,10,October,24,4,Friday,0,43
2025-10-25,400220,391763,49996,49678,318,2025,10,October,25,5,Saturday,1,43
2025-10-26,456848,416227,28683,28238,445,2025,10,October,26,6,Sunday,1,43
2025-10-27,369253,181332,26195,24964,1231,2025,10,October,27,0,Monday,0,44
2025-10-28,210471,229406,33808,32846,962,2025,10,October,28,1,Tuesday,0,44
2025-10-29,319050,346453,28930,27894,1036,2025,10,October,29,2,Wednesday,0,44
2025-10-30,420909,292844,116721,115594,1127,2025,10,October,30,3,Thursday,0,44
2025-10-31,445139,629254,71376,70259,1117,2025,10,October,31,4,Friday,0,44
2025-11-01,434459,473747,17849,17232,617,2025,11,November,1,5,Saturday,1,44
2025-11-02,405799,189470,100071,99752,319,2025,11,November,2,6,Sunday,1,44
2025-11-03,432804,481763,31532,30250,1282,2025,11,November,3,0,Monday,0,45
2025-11-04,288457,529256,1007,1001,6,2025,11,November,4,1,Tuesday,0,45
2025-11-05,356432,259667,75593,74843,750,2025,11,November,5,2,Wednesday,0,45
2025-11-06,418911,592307,43585,42070,1515,2025,11,November,6,3,Thursday,0,45
2025-11-07,370838,467099,42330,40904,1426,2025,11,November,7,4,Friday,0,45
2025-11-08,358073,479820,52390,51466,924,2025,11,November,8,5,Saturday,1,45
2025-11-09,231976,147772,48218,48039,179,2025,11,November,9,6,Sunday,1,45
2025-11-10,366974,496515,66984,65691,1293,2025,11,November,10,0,Monday,0,46
2025-11-11,414733,358414,44033,42820,1213,2025,11,November,11,1,Tuesday,0,46
2025-11-12,412672,543788,40496,38158,2338,2025,11,November,12,2,Wednesday,0,46
2025-11-13,367549,341409,33046,29978,3068,2025,11,November,13,3,Thursday,0,46
2025-11-14,265615,468250,46265,45064,1201,2025,11,November,14,4,Friday,0,46
2025-11-15,265574,432951,120087,119168,919,2025,11,November,15,5,Saturday,1,46
2025-11-16,292438,110111,53952,53526,426,2025,11,November,16,6,Sunday,1,46
2025-11-17,315850,366985,30687,29615,1072,2025,11,November,17,0,Monday,0,47
2025-11-18,413095,438487,70427,69048,1379,2025,11,November,18,1,Tuesday,0,47
2025-11-19,295974,437886,115029,110895,4134,2025,11,November,19,2,Wednesday,0,47
2025-11-25,576727,109523,58406,57285,1121,2025,11,November,25,1,Tuesday,0,48
2025-12-15,275701,346023,138883,133691,5192,2025,12,December,15,0,Monday,0,51
2025-12-22,39,263194,109337,109331,6,2025,12,December,22,0,Monday,0,52
2025-12-23,289,488407,47327,47291,36,2025,12,December,23,1,Tuesday,0,52
2025-12-25,547367,253374,48630,47210,1420,2025,12,December,25,3,Thursday,0,52
2025-12-26,450554,433711,52398,51482,916,2025,12,December,26,4,Friday,0,52
2025-12-27,430333,445894,53023,52019,1004,2025,12,December,27,5,Saturday,1,52
2025-12-28,151456,214482,45685,45443,242,2025,12,December,28,6,Sunday,1,52
2025-12-29,300391,276467,60684,59209,1475,2025,12,December,29,0,Monday,0,1"""

# 2. District Summary (Aggregated to State for Visual 2)
# Reading the CSV string (simulated)
df_daily = pd.read_csv(io.StringIO(daily_data))
df_daily['date'] = pd.to_datetime(df_daily['date'])

# For District/State summary I will load the provided sample data
# Since I can't load the large file directly in this script, I will use the daily national summary
# to simulate the state aggregation or load the provided district sample if it was large enough.
# However, the user provided a 'district_summary.csv' in the prompt, so let's load that.

district_data = """state,district,region,biometric_total,demographic_total,enrolment_total,child_enrolment,adult_enrolment,total_activity,bio_coverage_pct,child_share_pct
Maharashtra,Thane,MAHARASHTRA - THANE,458811.0,299319.0,40611.0,39698.0,913.0,798741.0,1129.77,97.75
Maharashtra,Pune,MAHARASHTRA - PUNE,471570.0,272698.0,28820.0,27747.0,1073.0,773088.0,1636.26,96.28
Maharashtra,Nashik,MAHARASHTRA - NASHIK,460419.0,168576.0,20056.0,19761.0,295.0,649051.0,2295.67,98.53
West Bengal,South 24 Parganas,WEST BENGAL - SOUTH 24 PARGANAS,184877.0,283790.0,30844.0,30562.0,282.0,499511.0,599.39,99.09
Gujarat,Ahmedabad,GUJARAT - AHMEDABAD,320804.0,159213.0,17271.0,16733.0,538.0,497288.0,1857.47,96.88
Gujarat,Surat,GUJARAT - SURAT,223522.0,247012.0,23800.0,23162.0,638.0,494334.0,939.17,97.32
Delhi,North West Delhi,DELHI - NORTH WEST DELHI,256168.0,218739.0,14632.0,14312.0,320.0,489539.0,1750.74,97.81
Rajasthan,Jaipur,RAJASTHAN - JAIPUR,281622.0,175994.0,28288.0,27585.0,703.0,485904.0,995.55,97.51
West Bengal,Murshidabad,WEST BENGAL - MURSHIDABAD,178817.0,271748.0,33131.0,33049.0,82.0,483696.0,539.73,99.75
Maharashtra,Nanded,MAHARASHTRA - NANDED,275745.0,182790.0,10812.0,10490.0,322.0,469347.0,2550.36,97.02"""

df_district = pd.read_csv(io.StringIO(district_data))

# 3. Lowest Coverage Regions
low_cov_data = """region,bio_total,bio_start,bio_end,bio_days,demo_total,enrol_total,child_count,adult_count,bio_coverage_pct
ASSAM - SIVASAGAR,0.0,0,0,0.0,0.0,422.0,317.0,105.0,0.0
KARNATAKA - BENGALURU URBAN,0.0,0,0,0.0,0.0,22342.0,18777.0,3565.0,0.0
MAHARASHTRA - AHMEDNAGAR,0.0,0,0,0.0,0.0,368.0,340.0,28.0,0.0
WEST BENGAL - 24 PARAGANAS NORTH,0.0,0,0,0.0,0.0,6147.0,5635.0,512.0,0.0
WEST BENGAL - DINAJPUR DAKSHIN,0.0,0,0,0.0,0.0,997.0,963.0,34.0,0.0
WEST BENGAL - DINAJPUR UTTAR,0.0,0,0,0.0,0.0,11600.0,11293.0,307.0,0.0
WEST BENGAL - COOCHBEHAR,0.0,0,0,0.0,0.0,4360.0,4196.0,164.0,0.0
ANDHRA PRADESH - SPSR NELLORE,0.0,0,0,0.0,0.0,2067.0,1793.0,274.0,0.0
WEST BENGAL - 24 PARAGANAS SOUTH,0.0,0,0,0.0,0.0,490.0,468.0,22.0,0.0
JHARKHAND - EAST SINGHBHUM,0.0,0,0,0.0,0.0,1447.0,1394.0,53.0,0.0"""

df_low_cov = pd.read_csv(io.StringIO(low_cov_data))

# 4. Delayed Regions (Lag Days)
delayed_data = """region,best_lag_days,correlation,data_points
ANDHRA PRADESH - ANANTAPUR,30,0.3438,70
ANDHRA PRADESH - ADILABAD,30,0.5977,70
ANDHRA PRADESH - WEST GODAVARI,30,0.2814,70
ARUNACHAL PRADESH - PAPUM PARE,30,0.2944,70
ANDHRA PRADESH - ANANTHAPURAMU,30,0.2418,70
ANDHRA PRADESH - ELURU,30,0.3423,70
ANDHRA PRADESH - DR. B. R. AMBEDKAR KONASEEMA,30,0.2331,70
ANDHRA PRADESH - CUDDAPAH,30,0.2593,70
ANDHRA PRADESH - CHITTOOR,30,0.2872,70
ANDHRA PRADESH - ANNAMAYYA,30,0.4010,70"""

df_delayed = pd.read_csv(io.StringIO(delayed_data))

# 5. Low Child Penetration
low_child_data = """region,child_count,adult_count,enrol_total,child_share
MEGHALAYA - EASTERN WEST KHASI HILLS,175.0,389.0,564.0,31.03
MEGHALAYA - RI BHOI,5740.0,3327.0,9067.0,63.31
MEGHALAYA - EAST JAINTIA HILLS,3256.0,1756.0,5012.0,64.96
MEGHALAYA - EAST KHASI HILLS,18244.0,9554.0,27798.0,65.63
MEGHALAYA - SOUTH GARO HILLS,2763.0,1444.0,4207.0,65.68
MEGHALAYA - WEST JAINTIA HILLS,7315.0,3617.0,10932.0,66.91
MEGHALAYA - SOUTH WEST KHASI HILLS,2277.0,1091.0,3368.0,67.61
PUNJAB - KAPURTHALA,2383.0,1137.0,3520.0,67.7
MEGHALAYA - WEST KHASI HILLS,10114.0,4800.0,14914.0,67.82
WEST BENGAL - KALIMPONG,342.0,151.0,493.0,69.37"""

df_low_child = pd.read_csv(io.StringIO(low_child_data))

# --- GENERATE VISUALIZATIONS ---

# PAGE 1: EXECUTIVE DASHBOARD
fig1 = plt.figure(figsize=(18, 10))
gs1 = fig1.add_gridspec(2, 2)

# 1.1 KPI Summary (Text)
ax1_1 = fig1.add_subplot(gs1[0, 0])
total_bio = df_daily['bio_total'].sum()
total_demo = df_daily['demo_total'].sum()
total_enrol = df_daily['enrol_total'].sum()

ax1_1.text(0.1, 0.7, f"Total Biometric\n{total_bio:,.0f}", fontsize=20, color=COLORS['bio'], fontweight='bold')
ax1_1.text(0.1, 0.4, f"Total Demographic\n{total_demo:,.0f}", fontsize=20, color=COLORS['demo'], fontweight='bold')
ax1_1.text(0.1, 0.1, f"Total Enrolment\n{total_enrol:,.0f}", fontsize=20, color=COLORS['enrol'], fontweight='bold')
ax1_1.axis('off')
ax1_1.set_title("Key Performance Indicators (KPIs)", fontsize=16)

# 1.2 Activity Split (Pie Chart)
ax1_2 = fig1.add_subplot(gs1[0, 1])
activities = [total_bio, total_demo, total_enrol]
labels = ['Biometric', 'Demographic', 'Enrolment']
ax1_2.pie(activities, labels=labels, colors=[COLORS['bio'], COLORS['demo'], COLORS['enrol']], autopct='%1.1f%%', startangle=140)
ax1_2.set_title("Total Activity Split", fontsize=14)

# 1.3 Daily Trends (Line Chart)
ax1_3 = fig1.add_subplot(gs1[1, :])
ax1_3.plot(df_daily['date'], df_daily['bio_total'], label='Biometric', color=COLORS['bio'])
ax1_3.plot(df_daily['date'], df_daily['demo_total'], label='Demographic', color=COLORS['demo'])
ax1_3.plot(df_daily['date'], df_daily['enrol_total'], label='Enrolment', color=COLORS['enrol'])
ax1_3.set_title("Daily Activity Trends (2025)", fontsize=14)
ax1_3.legend()
ax1_3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('page1_executive_dashboard.png')
plt.close()


# PAGE 2: GEOGRAPHIC ANALYSIS
# Using district_summary grouped by state for top states
df_state_agg = df_district.groupby('state')['total_activity'].sum().sort_values(ascending=False).head(10).reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_state_agg, x='total_activity', y='state', palette='viridis', ax=ax2)
ax2.set_title("Top 10 States by Total Activity", fontsize=16)
ax2.set_xlabel("Total Transactions")
plt.tight_layout()
plt.savefig('page2_geographic_analysis.png')
plt.close()


# PAGE 3: TIME ANALYSIS
fig3 = plt.figure(figsize=(18, 8))
gs3 = fig3.add_gridspec(1, 2)

# 3.1 Weekday vs Weekend (Bar Chart)
# Ensure order of days
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_weekday = df_daily.groupby('day_name')['bio_total'].mean().reindex(days_order).reset_index()

ax3_1 = fig3.add_subplot(gs3[0, 0])
sns.barplot(data=df_weekday, x='day_name', y='bio_total', color=COLORS['primary'], ax=ax3_1)
ax3_1.set_title("Average Biometric Activity by Day of Week", fontsize=14)
ax3_1.tick_params(axis='x', rotation=45)

# 3.2 Weekly Heatmap
# Creating a pivot for heatmap: Week Number vs Weekday
heatmap_data = df_daily.pivot_table(index='day_name', columns='week_num', values='bio_total', aggfunc='sum')
# Reorder rows
heatmap_data = heatmap_data.reindex(days_order)

ax3_2 = fig3.add_subplot(gs3[0, 1])
sns.heatmap(heatmap_data, cmap='Blues', ax=ax3_2, cbar_kws={'label': 'Biometric Count'})
ax3_2.set_title("Biometric Activity Heatmap (Day vs Week Num)", fontsize=14)

plt.tight_layout()
plt.savefig('page3_time_analysis.png')
plt.close()


# PAGE 4: COVERAGE & INSIGHTS
fig4 = plt.figure(figsize=(18, 12))
gs4 = fig4.add_gridspec(2, 2)

# 4.1 Scatter: Enrolment vs Bio Coverage
ax4_1 = fig4.add_subplot(gs4[0, 0])
sns.scatterplot(data=df_district, x='enrolment_total', y='bio_coverage_pct', hue='state', legend=False, ax=ax4_1)
ax4_1.set_title("Biometric Coverage % vs Total Enrolment (District Level)", fontsize=14)
ax4_1.set_xlabel("Total Enrolment")
ax4_1.set_ylabel("Biometric Coverage %")

# 4.2 Bar: Bottom 10 Regions by Coverage
ax4_2 = fig4.add_subplot(gs4[0, 1])
df_low_cov_sorted = df_low_cov.sort_values('bio_coverage_pct').head(10)
sns.barplot(data=df_low_cov_sorted, x='bio_coverage_pct', y='region', color=COLORS['alert'], ax=ax4_2)
ax4_2.set_title("Bottom 10 Regions by Biometric Coverage %", fontsize=14)

# 4.3 Bar: Top Delayed Regions (Lag Days)
ax4_3 = fig4.add_subplot(gs4[1, 0])
df_delayed_sorted = df_delayed.sort_values('best_lag_days', ascending=False).head(10)
sns.barplot(data=df_delayed_sorted, x='best_lag_days', y='region', color='orange', ax=ax4_3)
ax4_3.set_title("Regions with Highest Data Sync Lag (Days)", fontsize=14)

# 4.4 Bar: Lowest Child Penetration
ax4_4 = fig4.add_subplot(gs4[1, 1])
df_low_child_sorted = df_low_child.sort_values('child_share').head(10)
sns.barplot(data=df_low_child_sorted, x='child_share', y='region', color='teal', ax=ax4_4)
ax4_4.set_title("Regions with Lowest Child Enrolment Share (%)", fontsize=14)

plt.tight_layout()
plt.savefig('page4_coverage_insights.png')
plt.close()

print("Graphs generated successfully:")
print("1. page1_executive_dashboard.png")
print("2. page2_geographic_analysis.png")
print("3. page3_time_analysis.png")
print("4. page4_coverage_insights.png")