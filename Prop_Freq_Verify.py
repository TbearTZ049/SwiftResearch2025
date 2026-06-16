"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
Created on Fri Nov  8 20:23:55 2024
@author: catermurawski

SUMMARY OF FILE:
This file is responsible for verifying the proportions of pulse shape
classifications for each burst. It reads the PulseShapes.csv file, calculates
the relative proportions of each classification category (Simple, Extended, 
Other, Too Noisy), and determines if any category meets the criteria for 
verification based on the highest proportion (> 70%) and confidence intervals 
(95% and 99%). Also, checks for double category or no category cases. 
"""

import pandas as pd
import numpy as np

# Read in the file
file = pd.read_csv("CSVExports/Pulse_Shapes.csv")

# Calculate proportions for each category
simple_prop = file["Simple"] / (file["Simple"] + file["Extended"] + file["Other"] + file["Too_Noisy"])
ext_prop = file["Extended"] / (file["Simple"] + file["Extended"] + file["Other"] + file["Too_Noisy"])
oth_prop = file["Other"] / (file["Simple"] + file["Extended"] + file["Other"] + file["Too_Noisy"])
tn_prop = file["Too_Noisy"] / (file["Simple"] + file["Extended"] + file["Other"] + file["Too_Noisy"])

# Combine data into a dictionary for processing
categories = {
    "Simple": simple_prop,
    "Extended": ext_prop,
    "Other": oth_prop,
    "Too_Noisy": tn_prop
}

# Calculate mean and standard deviation for each category
category_stats = {
    category: {
        "mean": np.mean(proportions),
        "std_dev": np.std(proportions),
    }
    for category, proportions in categories.items()
}

# Z-scores for 95% and 99% confidence intervals
confidence_levels = {
    "95%": 1.96,
    "99%": 2.58
}

# Prepare results DataFrame
results = []

# Process each burst individually
for idx, row in file.iterrows():
    if pd.isna(row["Burst_PNG"]) or str(row["Burst_PNG"]).strip() == "None":
        png = "None"
    else:
        png = row["Burst_PNG"]

    burst_results = {
        "Burst_Name": row["Burst_Name"],
        "Burst_PNG" :png,           
        "Simple": row["Simple"],
        "Extended": row["Extended"],
        "Other": row["Other"],
        "Too_Noisy": row["Too_Noisy"],
        "Count": row["Simple"]+row["Extended"]+row["Other"]+row["Too_Noisy"],
        "Simple_Proportion": round(simple_prop.iloc[idx], 3),
        "Extended_Proportion": round(ext_prop.iloc[idx], 3),
        "Other_Proportion": round(oth_prop.iloc[idx], 3),
        "Too_Noisy_Proportion": round(tn_prop.iloc[idx], 3),
        "Follow": row["Follow"],
        "95%_Verify": [],
        "99%_Verify": [],
    }

    # Calculate `Prop_Verify` based on the highest proportion > 70%
    proportions = {
    "Simple": simple_prop.iloc[idx],
    "Extended": ext_prop.iloc[idx],
    "Other": oth_prop.iloc[idx],
    "Too_Noisy": tn_prop.iloc[idx]
    }

    # Initialize prop_verify
    prop_verify = None

    # Find categories with proportions >= 40%
    over_40 = [category for category, proportion in proportions.items() if proportion > 0.4]

    # Check for a category >= 70%
    for category, proportion in proportions.items():
        if proportion >= 0.7:
            prop_verify = category
            break

    # If no category >= 70%, and two categories > 40%, join their names
    if not prop_verify and len(over_40) == 2:
        prop_verify = "/".join(over_40)

    # If no category >= 70% and no two categories > 40%, set "None"
    if not prop_verify:
        prop_verify = "None"

    # Assign to burst_results
    burst_results["Prop_Verify"] = prop_verify

    # Check if the burst's proportions fall in the 95% and 99% confidence intervals
    for category, stats in category_stats.items():
        std_dev = stats["std_dev"]
        proportion = proportions[category]

        for conf, z_score in confidence_levels.items():
            if proportion > 0 + z_score * std_dev:  # Check if beyond confidence threshold
                burst_results[f"{conf}_Verify"].append(category)

    # Flatten verification results into formatted strings
    burst_results["95%_Verify"] = (
        "/".join(burst_results["95%_Verify"]) if len(burst_results["95%_Verify"]) > 1 else 
        ", ".join(burst_results["95%_Verify"]) if burst_results["95%_Verify"] else "None"
    )
    burst_results["99%_Verify"] = (
        "/".join(burst_results["99%_Verify"]) if len(burst_results["99%_Verify"]) > 1 else 
        ", ".join(burst_results["99%_Verify"]) if burst_results["99%_Verify"] else "None"
    )

    # Append result for this burst
    results.append(burst_results)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to a CSV file
results_df.to_csv(f'ClassifiedBursts/Verified_Prop_Freq.csv', index=True, header=True)
print("Analysis complete. Results saved to CSV.")
