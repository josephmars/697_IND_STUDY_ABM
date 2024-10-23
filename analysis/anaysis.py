import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load BehaviorSpace data
data = pd.read_csv('results/runs_results_processed.csv')

# Check data columns
print("Data Columns:")
print(data.columns)

# Compute average final proportion of grammar 1 users for each parameter combination
grouped_data = data.groupby(['prestige', 'threshold-val']).agg({
    'final-grammar1-proportion': ['mean', 'std'],
    'ticks': ['mean', 'std']
}).reset_index()

# Flatten MultiIndex columns
grouped_data.columns = ['prestige', 'threshold-val',
                        'mean_final_prop', 'std_final_prop',
                        'mean_ticks', 'std_ticks']

# Save summarized data to CSV
grouped_data.to_csv('summarized_results.csv', index=False)

# Display summarized data
print("\nSummarized Data:")
print(grouped_data)

# Correlation Analysis
corr_matrix = data[['prestige', 'threshold-val', 'final-grammar1-proportion', 'ticks']].corr()

print("\nCorrelation Matrix:")
print(corr_matrix)

# Plotting Correlation Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='Blues')
plt.title('Correlation Matrix Heatmap')
plt.show()

# Scatter Plot: Prestige vs Final Proportion
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='prestige', y='final-grammar1-proportion', hue='threshold-val', palette='viridis')
plt.title('Prestige vs Final Proportion of Grammar 1')
plt.xlabel('Prestige of Grammar 1')
plt.ylabel('Final Proportion of Grammar 1 Users')
plt.legend(title='Threshold Value')
plt.show()

# Scatter Plot: Threshold Value vs Final Proportion
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='threshold-val', y='final-grammar1-proportion', hue='prestige', palette='plasma')
plt.title('Threshold Value vs Final Proportion of Grammar 1')
plt.xlabel('Threshold Value')
plt.ylabel('Final Proportion of Grammar 1 Users')
plt.legend(title='Prestige')
plt.show()
