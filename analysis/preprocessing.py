import pandas as pd

def preprocess_behaviorspace_output(input_file, output_file):
    # Read the CSV file line by line
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            # Split each line by tabs
            row = line.strip().split('\t')
            data.append(row)

    # Find indices for '[reporter]' and '[all run data]'
    reporter_index = None
    all_run_data_index = None
    for i, row in enumerate(data):
        if row and row[0] == '[reporter]':
            reporter_index = i
        elif row and row[0] == '[all run data]':
            all_run_data_index = i
            break  # Assuming '[all run data]' comes after '[reporter]'

    # Calculate the number of runs
    num_cols = max(len(row) for row in data)
    num_runs = (num_cols - 1) // 2

    # Initialize a list to store data for each run
    runs_data = []

    for run_idx in range(num_runs):
        run_data = {}
        col_step = 1 + 2 * run_idx     # Column for steps
        col_value = col_step + 1       # Column for values

        # Get run number from the first row
        run_number = data[0][col_step]
        run_data['run_number'] = int(run_number)

        # Get parameters from rows before '[reporter]'
        for row in data[1:reporter_index]:
            param_name = row[0]
            param_value = row[col_step]
            # Handle missing values by checking the next column
            if not param_value and len(row) > col_value:
                param_value = row[col_value]
            run_data[param_name] = param_value

        # Get output values from the '[final]' row
        for i in range(reporter_index + 1, all_run_data_index):
            row = data[i]
            if row[0] == '[final]':
                # Get the output value
                if len(row) > col_value:
                    output_value = row[col_value]
                    run_data['final_output'] = output_value
                else:
                    run_data['final_output'] = None
                break
        else:
            # If '[final]' not found, set output as None
            run_data['final_output'] = None

        runs_data.append(run_data)

    # Create a DataFrame from the runs data
    df_runs = pd.DataFrame(runs_data)

    # Convert parameter values to appropriate data types
    # Replace 'prestige', 'threshold-val', etc., with actual parameter names
    for param in ['prestige', 'threshold-val', 'alpha', 'percent-grammar-1', 'num-nodes']:
        if param in df_runs.columns:
            df_runs[param] = pd.to_numeric(df_runs[param], errors='coerce')

    # Convert 'final_output' to numeric
    df_runs['final_output'] = pd.to_numeric(df_runs['final_output'], errors='coerce')

    # Save the processed data to a new CSV file
    df_runs.to_csv(output_file, index=False)
    print(f"Processed data saved to '{output_file}'")

if __name__ == "__main__":
    input_file = '/Users/joseph/Library/CloudStorage/OneDrive-OldDominionUniversity/MS Modeling and Simulation/2024-30/697 INDEPENDENT STUDY ABM/results/Language Change with Prestige Prestige_Threshold_Experiment-spreadsheet.csv'
    output_file = '/Users/joseph/Library/CloudStorage/OneDrive-OldDominionUniversity/MS Modeling and Simulation/2024-30/697 INDEPENDENT STUDY ABM/results/runs_results_processed.csv'

    preprocess_behaviorspace_output(input_file, output_file)
