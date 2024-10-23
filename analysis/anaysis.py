import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed CSV data
data = pd.read_csv('/Users/joseph/Library/CloudStorage/OneDrive-OldDominionUniversity/MS Modeling and Simulation/2024-30/697 INDEPENDENT STUDY ABM/results/runs_results_processed.csv')

# Ensure correct data types
data['prestige'] = data['prestige'].astype(float)
data['threshold'] = data['threshold'].astype(float)
data['output'] = data['output'].astype(float)

# Check data columns
print("Data Columns:")
print(data.columns)

# Keep only the final step for each run
# First, find the maximum step number for each run
max_steps = data.groupby(['run_number', 'prestige', 'threshold'])['step'].max().reset_index()

# Merge with the original data to get the rows corresponding to the final step
final_steps = pd.merge(data, max_steps, on=['run_number', 'prestige', 'threshold', 'step'])

# Now, we have the data for the final step of each run
# Group by prestige and threshold to compute mean and std
grouped_data = final_steps.groupby(['prestige', 'threshold']).agg({
    'output': ['mean', 'std']
}).reset_index()

# Flatten MultiIndex columns
grouped_data.columns = ['prestige', 'threshold', 'mean_final_output', 'std_final_output']

# Save summarized data to CSV
grouped_data.to_csv('summarized_results.csv', index=False)

# Display summarized data
print("\nSummarized Data:")
print(grouped_data)

# Correlation Analysis
corr_matrix = final_steps[['prestige', 'threshold', 'output']].corr()

print("\nCorrelation Matrix:")
print(corr_matrix)

# Plotting Correlation Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='Blues')
plt.title('Correlation Matrix Heatmap')
plt.show()

# Scatter Plot: Prestige vs Final Output
plt.figure(figsize=(8, 6))
sns.scatterplot(data=final_steps, x='prestige', y='output', hue='threshold', palette='viridis')
plt.title('Prestige vs Final Output')
plt.xlabel('Prestige')
plt.ylabel('Final Output')
plt.legend(title='Threshold')
plt.show()

# Scatter Plot: Threshold vs Final Output
plt.figure(figsize=(8, 6))
sns.scatterplot(data=final_steps, x='threshold', y='output', hue='prestige', palette='plasma')
plt.title('Threshold vs Final Output')
plt.xlabel('Threshold')
plt.ylabel('Final Output')
plt.legend(title='Prestige')
plt.show()
