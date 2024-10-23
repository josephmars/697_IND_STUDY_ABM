import pandas as pd

def preprocess_behaviorspace_output(n_runs, input_file, output_file):
    # Read the CSV file into a DataFrame, specifying that headers are not present
    df_raw = pd.read_csv(input_file)
    # Create an empty DataFrame to store the processed data with the colums step, run_number, prestige, threshold, and output.
    output_list = []
    
    
    print(df_raw.shape)
    print(df_raw.head(50))
    idx_prestige = 1
    idx_threshold = 7
    start_values_idx = 15
    end_values_idx = 116
    for column in df_raw.columns[1:]:
        run = str(column).replace('.1', '')# if there is a .1 at the end, it is the outpur value, otherwise it is the step number
        if run == str(column):
            prestige = df_raw[column][idx_prestige]
            threshold = df_raw[column][idx_threshold]
        else:
            step = 0
            for i in range(start_values_idx, end_values_idx):
                output = df_raw[column][i]
                output_list.append({'step': step, 'run_number': run, 'prestige': prestige, 'threshold': threshold, 'output': output})
                step += 1
    
    # Save to CSV
    pd.DataFrame(output_list).to_csv(output_file, index=False)
    print(f"Processed data saved to '{output_file}'")

if __name__ == "__main__":
    n_runs = 900
    input_file = '/Users/joseph/Library/CloudStorage/OneDrive-OldDominionUniversity/MS Modeling and Simulation/2024-30/697 INDEPENDENT STUDY ABM/results/Language Change with Prestige Prestige_Threshold_Experiment-spreadsheet.csv'
    output_file = '/Users/joseph/Library/CloudStorage/OneDrive-OldDominionUniversity/MS Modeling and Simulation/2024-30/697 INDEPENDENT STUDY ABM/results/runs_results_processed.csv'

    preprocess_behaviorspace_output(n_runs, input_file, output_file)
