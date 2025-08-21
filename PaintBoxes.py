import os
import pandas as pd
from PIL import Image, ImageDraw

# Input/Output paths
results_file = "ClassifiedBursts/Pulse_Location_Narrowed.csv"
image_folder = "BurstPhotos"  # Path where the PNGs are stored
output_folder = "BurstBoxes"  # Folder to save boxed images

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load results from CSV
df = pd.read_csv(results_file)

# Group results by burst name
grouped = df.groupby("Burst Name")

# Loop through each group (burst name)
for burst_name, group in grouped:
    # Find the corresponding PNG file containing the burst name
    matching_files = [f for f in os.listdir(image_folder) if burst_name in f and f.endswith(".png")]

    if not matching_files:
        print(f"❌ No matching PNG found for {burst_name}")
        continue

    # Loop through matching files (in case of multiple)
    for png_file in matching_files:
        png_path = os.path.join(image_folder, png_file)

        # Open the PNG file
        try:
            image = Image.open(png_path)
        except Exception as e:
            print(f"❌ Error opening {png_path}: {e}")
            continue

        draw = ImageDraw.Draw(image)
        valid_box_found = False

        # Loop through each box in the group and draw on the same image
        for i, row in group.iterrows():
            x_min, y_min, x_max, y_max = row["x_min"], row["y_min"], row["x_max"], row["y_max"]

            # Check for valid box values (skip if NaN or invalid)
            if pd.isnull(x_min) or pd.isnull(y_min) or pd.isnull(x_max) or pd.isnull(y_max):
                print(f"⚠️ Skipping invalid box for {burst_name} (Row {i}) due to NaN values.")
                continue

            # Validate box dimensions
            if x_max <= x_min or y_max <= y_min:
                print(f"⚠️ Skipping invalid box with incorrect dimensions for {burst_name} (Row {i}).")
                continue

            # Draw the bounding box (red box with 3px thickness)
            box = [x_min, y_min, x_max, y_max]
            draw.rectangle(box, outline="red", width=3)
            valid_box_found = True

        # Save the image if any valid boxes were drawn
        if valid_box_found:
            output_path = os.path.join(output_folder, f"{os.path.splitext(png_file)[0]}_boxed.png")
            image.save(output_path)
            print(f"✅ Saved boxed image with multiple boxes for {burst_name} at {output_path}")
        else:
            print(f"⚠️ No valid boxes found for {burst_name}, skipping save...")

print("🎉 All bounding boxes added and images saved in 'Boxes'!")
