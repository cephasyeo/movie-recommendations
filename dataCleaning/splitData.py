import pandas as pd
from sklearn.model_selection import train_test_split

# Load the CSV file
file_path = "combined_data_with_embeddings.csv" 
df = pd.read_csv(file_path)

# Shuffle and split the dataset
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Save the subsets to new CSV files
train.to_csv("train_data.csv", index=False)
test.to_csv("test_data.csv", index=False)

# Output confirmation
print(f"Training set size: {len(train)} rows")
print(f"Testing set size: {len(test)} rows")
