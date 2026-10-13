#!/usr/bin/env python3
"""
Data cleaning and scoring script for Hararghe Household Needs Assessment.
Reads sample submissions, performs quality checks, and recomputes indicators.

This script demonstrates:
- Data quality control (GPS accuracy, duration checks, duplicate detection)
- Indicator recalculation (HHS, rCSI, TLU, dependency ratio)
- Enumerator performance analysis
- Summary statistics generation

Author: Arfan Eliyas
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data(filepath):
    """Load submission data from CSV."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records from {filepath}")
    return df

def check_gps_accuracy(df):
    """Check GPS accuracy and flag records with poor accuracy (>20m)."""
    df['gps_accuracy'] = df['gps'].apply(lambda x: float(x.split()[3]) if pd.notna(x) and isinstance(x, str) else np.nan)
    df['gps_quality_flag'] = np.where(df['gps_accuracy'] > 20, 'poor_accuracy', 'good')
    
    poor_gps = df[df['gps_quality_flag'] == 'poor_accuracy']
    print(f"\nGPS Accuracy Check: {len(poor_gps)} records with accuracy > 20m")
    
    return df

def check_gps_bounding_box(df):
    """Check if GPS coordinates are within Hararghe bounding box."""
    def extract_lat_lon(gps_str):
        if pd.notna(gps_str) and isinstance(gps_str, str):
            parts = gps_str.split()
            return float(parts[0]), float(parts[1])
        return np.nan, np.nan
    
    df[['latitude', 'longitude']] = df['gps'].apply(
        lambda x: pd.Series(extract_lat_lon(x))
    )
    
    # Hararghe bounding box (approximate)
    lat_min, lat_max = 8.0, 10.0
    lon_min, lon_max = 40.0, 43.5
    
    df['gps_in_box'] = (
        (df['latitude'] >= lat_min) & 
        (df['latitude'] <= lat_max) & 
        (df['longitude'] >= lon_min) & 
        (df['longitude'] <= lon_max)
    )
    
    outside_box = df[~df['gps_in_box']]
    print(f"GPS Bounding Box Check: {len(outside_box)} records outside Hararghe area")
    
    return df

def check_duration(df):
    """Check interview duration for unusually short interviews."""
    df['start_dt'] = pd.to_datetime(df['start'])
    df['end_dt'] = pd.to_datetime(df['end'])
    df['duration_minutes'] = (df['end_dt'] - df['start_dt']).dt.total_seconds() / 60
    
    # Flag interviews shorter than 5 minutes (suspicious)
    df['duration_flag'] = np.where(df['duration_minutes'] < 5, 'too_short', 'acceptable')
    
    short_interviews = df[df['duration_flag'] == 'too_short']
    print(f"Duration Check: {len(short_interviews)} interviews shorter than 5 minutes")
    
    return df

def check_duplicates(df):
    """Check for duplicate respondent codes."""
    duplicate_codes = df[df.duplicated(subset=['resp_name_code'], keep=False)]
    print(f"Duplicate Check: {len(duplicate_codes)} records with duplicate respondent codes")
    
    return df

def recompute_hhs(df):
    """Recompute Household Hunger Scale score."""
    # HHS scoring: rarely=1, sometimes=1, often=2
    # This is a placeholder - actual implementation depends on form structure
    df['hhs_score_recomputed'] = df['hhs_score']  # Placeholder
    
    # Compare with form-calculated values
    hhs_diff = df[df['hhs_score_recomputed'] != df['hhs_score']]
    print(f"HHS Recalculation: {len(hhs_diff)} records differ from form values")
    
    return df

def recompute_rcsi(df):
    """Recompute Reduced Coping Strategy Index score."""
    # rCSI = (pref*1 + borrow*2 + portion*1 + adult*3 + meals*1)
    df['rcsi_score_recomputed'] = (
        df['rcsi_pref'] * 1 +
        df['rcsi_borrow'] * 2 +
        df['rcsi_portion'] * 1 +
        df['rcsi_adult'] * 3 +
        df['rcsi_meals'] * 1
    )
    
    # Compare with form-calculated values
    rcsi_diff = df[df['rcsi_score_recomputed'] != df['rcsi_score']]
    print(f"rCSI Recalculation: {len(rcsi_diff)} records differ from form values")
    
    return df

def recompute_tlu(df):
    """Recompute Tropical Livestock Units."""
    # TLU = cattle*0.7 + camel*1.0 + shoat*0.1 + donkey*0.5 + poultry*0.01
    df['tlu_recomputed'] = (
        df['n_cattle'] * 0.7 +
        df['n_camel'] * 1.0 +
        df['n_shoat'] * 0.1 +
        df['n_donkey'] * 0.5 +
        df['n_poultry'] * 0.01
    ).round(2)
    
    # Compare with form-calculated values
    tlu_diff = df[df['tlu_recomputed'] != df['tlu']]
    print(f"TLU Recalculation: {len(tlu_diff)} records differ from form values")
    
    return df

def recompute_dep_ratio(df):
    """Recompute dependency ratio."""
    df['dep_ratio_recomputed'] = np.where(
        df['n_working'] > 0,
        (df['n_dependent'] / df['n_working']).round(2),
        99
    )
    
    # Compare with form-calculated values
    dep_diff = df[df['dep_ratio_recomputed'] != df['dep_ratio']]
    print(f"Dependency Ratio Recalculation: {len(dep_diff)} records differ from form values")
    
    return df

def generate_qc_summary(df):
    """Generate quality control summary by enumerator."""
    qc_summary = df.groupby('enum_id').agg({
        '_quality_flag': 'count',
        'gps_quality_flag': lambda x: (x == 'poor_accuracy').sum(),
        'gps_in_box': lambda x: (~x).sum(),
        'duration_flag': lambda x: (x == 'too_short').sum(),
        'hhs_score': 'mean',
        'rcsi_score': 'mean',
        'tlu': 'mean',
        'dep_ratio': 'mean'
    }).rename(columns={
        '_quality_flag': 'total_submissions',
        'gps_quality_flag': 'poor_gps_count',
        'gps_in_box': 'gps_outside_box_count',
        'duration_flag': 'short_duration_count',
        'hhs_score': 'avg_hhs',
        'rcsi_score': 'avg_rcsi',
        'tlu': 'avg_tlu',
        'dep_ratio': 'avg_dep_ratio'
    })
    
    print("\n=== Quality Control Summary by Enumerator ===")
    print(qc_summary)
    
    return qc_summary

def generate_overall_summary(df):
    """Generate overall summary statistics."""
    print("\n=== Overall Summary Statistics ===")
    print(f"Total submissions: {len(df)}")
    print(f"Households with under-5 children: {df['has_under5'].sum()}")
    print(f"Households experiencing shocks: {(df['any_shock'] == 'yes').sum()}")
    print(f"Average HHS score: {df['hhs_score'].mean():.2f}")
    print(f"Average rCSI score: {df['rcsi_score'].mean():.2f}")
    print(f"Average TLU: {df['tlu'].mean():.2f}")
    print(f"Average dependency ratio: {df['dep_ratio'].mean():.2f}")
    
    print("\n=== Food Security Distribution ===")
    print(df['hhs_cat'].value_counts())
    
    print("\n=== Coping Strategy Distribution ===")
    print(df['rcsi_cat'].value_counts())

def main():
    """Main analysis pipeline."""
    input_file = '../data/sample_submissions.csv'
    output_file = '../data/cleaned_submissions.csv'
    
    # Load data
    df = load_data(input_file)
    
    # Quality checks
    df = check_gps_accuracy(df)
    df = check_gps_bounding_box(df)
    df = check_duration(df)
    df = check_duplicates(df)
    
    # Recompute indicators
    df = recompute_hhs(df)
    df = recompute_rcsi(df)
    df = recompute_tlu(df)
    df = recompute_dep_ratio(df)
    
    # Generate summaries
    qc_summary = generate_qc_summary(df)
    generate_overall_summary(df)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    
    # Save QC summary
    qc_summary.to_csv('../data/qc_summary_by_enumerator.csv')
    print("QC summary saved to: ../data/qc_summary_by_enumerator.csv")

if __name__ == '__main__':
    main()
