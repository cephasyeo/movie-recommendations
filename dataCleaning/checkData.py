import pandas as pd

# Load the CSV file into a pandas DataFrame
csv_file = 'combined_data_with_embeddings.csv'  # Replace with your file path
df = pd.read_csv(csv_file)

# Check for null or missing values in each column
nulls = df.isnull().sum()

# Print columns with nulls
if nulls.any():
    print("Columns with null or missing values:")
    print(nulls[nulls > 0])
else:
    print("No null or missing values found in any column.")
