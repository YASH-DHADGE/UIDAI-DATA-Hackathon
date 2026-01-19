"""
UIDAI Data Hackathon 2026 - Complete Analysis Script
Comprehensive analysis of anonymized Aadhaar enrolment and update datasets

Author: UIDAI Data Hackathon 2026 Participant
Date: January 2026

Run this script from the project root directory:
    cd "d:\Aadhar data hackathon"
    python src/complete_analysis.py
"""

# Execute all analysis parts in sequence
import os
import sys

# Set working directory to src folder parent
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)
sys.path.insert(0, project_root)

print("=" * 70)
print("UIDAI DATA HACKATHON 2026 - COMPLETE ANALYSIS")
print("=" * 70)
print(f"\nProject Root: {project_root}")
print(f"Working Directory: {os.getcwd()}")

# Import and run each part
print("\n📥 Loading analysis modules...")

exec(open('src/analysis_part1_loading.py').read())
exec(open('src/analysis_part2_preprocessing.py').read())
exec(open('src/analysis_part3_visualizations.py').read())
exec(open('src/analysis_part4_bivariate.py').read())
exec(open('src/analysis_part5_trivariate.py').read())
exec(open('src/analysis_part6_advanced.py').read())
exec(open('src/analysis_part7_insights.py').read())

print("\n" + "=" * 70)
print("🎉 ALL ANALYSIS COMPLETE!")
print("=" * 70)
print(f"\n📁 Check 'visualizations/' folder for all generated charts")
print(f"📊 Total visualizations: 16+")
print(f"📝 Key insights saved to 'visualizations/KEY_INSIGHTS.txt'")
print(f"📋 Recommendations saved to 'visualizations/RECOMMENDATIONS.txt'")
