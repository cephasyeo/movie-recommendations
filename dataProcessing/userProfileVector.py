""" to create user profile, this user profile is an agg representation of the user preferences"""

import pandas as pd
import numpy as np

def calculate_user_profiles(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    # right now embeddings are in string, covert to numeric array
    df['movie_embeddings'] = df['movie_embeddings'].apply(eval)

    # group by userID
    user_profiles = {}

    for user_id, group in df.groupby('userId'):
        # extract movie embeddings and ratings for the user
        embeddings = np.array(group['movie_embeddings'].tolist()) # matrix of embedding
        ratings = group['rating'].values.reshape(-1, 1) # column vector of ratings

        # weighted sum of movie embeddings
        weighted_sum = np.sum(embeddings * ratings, axis=0)

        # normalize sum of ratings
        user_profile = weighted_sum / np.sum(ratings)

        # save profile
        user_profiles[user_id] = user_profile

    # Convert user profiles to a DataFrame
    user_profiles_df = pd.DataFrame.from_dict(user_profiles, orient='index')
    user_profiles_df.reset_index(inplace=True)
    user_profiles_df.rename(columns={'index': 'userId'}, inplace=True)

    # Save user profiles to a CSV file
    user_profiles_df.to_csv(output_csv, index=False)
    print(f"User profiles saved to {output_csv}")

user_profiles = calculate_user_profiles('train_wo_userprofile.csv', 'user_profiles.csv')