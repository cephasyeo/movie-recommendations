""" split data evenly. such that for user x, x's records are split with 70% training, 15% validation, and 15% test """

import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv("final_data.csv")

def split_user_data(user_data, train_ratio, test_ratio, val_ratio):
    """
    splits a single user's data into train, validation, and test sets
    """
    # split data into 2
    train_data, temp_data = train_test_split(user_data, test_size=(1-train_ratio), random_state=42)
    # split temp_data into 2
    val_data, test_data = train_test_split(temp_data, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=42)

    return train_data, val_data, test_data

# init empty dfs
train_set = pd.DataFrame(columns=data.columns)
val_set = pd.DataFrame(columns=data.columns)
test_set = pd.DataFrame(columns=data.columns)

# ratios for splitting
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

print("splitting...")

# group by userID and split each user's data
for user_id, user_data in data.groupby("userId"):
    train_data, val_data, test_data = split_user_data(user_data, train_ratio, test_ratio, val_ratio)
    train_set = pd.concat([train_set, train_data])
    val_set = pd.concat([val_set, val_data])
    test_set = pd.concat([test_set, test_data])

train_set.to_csv("train_set.csv", index=False)
val_set.to_csv("val_set.csv", index=False)
test_set.to_csv("test_set.csv", index=False)

print("done saving")