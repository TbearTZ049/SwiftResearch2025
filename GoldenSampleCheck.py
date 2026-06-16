"""
SUMMARY OF FILE:
This file compares the scientist-verified GRB classifications (from AnswerKey.csv) with 
the machine learning classifications (from pulse_shape_freq_with_ml.csv). It checks for 
matches and mismatches between the two sets of classifications and provides a summary of 
the results, including a table of any mismatches for further review/follow-up.
"""

import pandas as pd

# File paths
human_file = "CSVExports/AnswerKey.csv"  # <-- replace with your actual file name if different
ml_file = "MachineLearning/pulse_shape_freq_with_ml.csv"

# Load data frames
human_df = pd.read_csv(human_file)
ml_df = pd.read_csv(ml_file)

# Rename column for consistent merging
human_df = human_df.rename(columns={"GRB_Name": "Burst_Name"})

# Merge on Burst_Name / GRB_Name
merged = pd.merge(human_df, ml_df[["Burst_Name", "ML_Verify"]], on="Burst_Name", how="inner")

# Compare Question_1 to ML_Verify
merged["Match"] = merged["Question_1"].str.strip() == merged["ML_Verify"].str.strip()

# Stats
total = len(merged) # Total number of compared entries
matches = merged["Match"].sum() # Number of matches
mismatches = total - matches # Number of mismatches

# Show mismatch table (optional)
mismatch_table = merged[~merged["Match"]][["Burst_Name", "Question_1", "ML_Verify"]]

# Print results
print(f"Total Compared: {total}")
print(f"Matches: {matches}")
print(f"Mismatches: {mismatches}")
print("\nMismatches:")
print(mismatch_table.to_string(index=False))
