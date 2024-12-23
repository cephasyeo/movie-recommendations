import pandas as pd

def check_column_data_types(csv_file, column_name):
    try:
        # Read the CSV file
        data = pd.read_csv(csv_file)
        
        if column_name not in data.columns:
            print(f"Column '{column_name}' not found in the CSV.")
            return

        # Check data types in the column
        data_types = data[column_name].map(type).value_counts()

        print(f"Data types in column '{column_name}':")
        for dtype, count in data_types.items():
            print(f"{dtype}: {count}")
            
    except FileNotFoundError:
        print(f"File '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file = "train_wo_userprofile.csv"  # Replace with your CSV file path
column_name = "movie_embeddings"  # Replace with the column name you want to check
check_column_data_types(csv_file, column_name)
