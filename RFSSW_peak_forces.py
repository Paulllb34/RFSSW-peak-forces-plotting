# Paul Blackhurst, EWI, 2024
# 
# This script will take a root folder of RFSSW weld .csv files (including nested
# folders) and plot the max or min (change lines 64-65) force values from each file.
# 
# This should work for any weld file produced on the BOND RFSSW machine.

# y-axis limits and plot title
y_min = 0
y_max = 15000
title = 'RFSSW Peak Weld Forces'

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Specify the path to the root folder, pull every csv file, organize by date, and save in csv_files.
root_folder = "/Users/paulblackhurst/Desktop/Python/IA scripts test/Python Scripts/RFSSW_peak_forces/Welds"
csv_files = []
for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(root, file))

# Function for ordering weld files using the file name produced by BOND RFSSW machine.
def extract_date(file_path):
    file_name = os.path.basename(file_path)
    date_part = file_name.split('_')[1:7]  # Extract date components
    date_str = ''.join(date_part)  # Concatenate to form a single string
    return date_str

csv_files.sort(key = extract_date)

# Create empty lists for appending values.
msf_max_weld = [] # Shoulder values
msp_max_weld = [] # Probe values

# Variable used for tracking script execution progress (see bottom of for-loop).
p = 0

# Loop through files and pull max values froms specified columns.
for file in csv_files:

    df = pd.read_csv(file)

    # Take the desired columns from the data frame and save them as numpy arrays.
    msf = np.array(df['Shoulder Force (N) ()'])
    mpf = np.array(df['Probe Force (N) ()'])

    # Used for separating weld sections below.
    sh_pos = np.array(df['Shoulder (Y) Pos (mm) ()'])

    # Find the data points that separate the pre-weld, weld, and cleaning cycle forces.
    neg_idx = np.where(sh_pos < 0)[0]
    split_1 = neg_idx[0]
    split_2 = neg_idx[-1]

    # Filter data so you only have weld data points (filters out pre-weld and cleaning cycle).
    msf_weld = msf[split_1:split_2]
    mpf_weld = mpf[split_1:split_2]

    # Append the max value from the filtered data to the lists below for plotting.
    msf_max_weld.append(np.max(msf_weld))
    msp_max_weld.append(np.max(mpf_weld))

    p = p + 1
    a = (p/len(csv_files)) * 100
    print(f"{a:.1f}%")

## FIGURE 1

# Create figure, specifiy dimensions, x-axis, transparency of grid.
fig1, ax1 = plt.subplots(figsize=(20, 5))
x = list(range(1,len(csv_files)+1))
plt.xticks(np.arange(0, len(csv_files)+18, step=48), fontsize=8, rotation=45)
plt.grid(True, alpha=0.4)

# Plot force data on the left y-axis.
ax1.plot(x, msf_max_weld, label='Max Shoulder Force', color='tab:blue',
            marker='o', linestyle='solid', linewidth=0.5, markersize=1)
ax1.plot(x, msp_max_weld, label='Max Probe Force', color='tab:red',
            marker='o', linestyle='solid', linewidth=0.5, markersize=1)
ax1.set_xlabel('Weld #')
ax1.set_ylabel('Max Force (N)', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_ylim(y_min,y_max)
ax1.legend(loc='center', bbox_to_anchor=(0.86, 0.90), framealpha=1)
ax1.set_title(title)

# Save the plot as a PNG image with higher resolution (300 dpi).
fig1.savefig(os.path.join(root_folder, title), dpi=300)