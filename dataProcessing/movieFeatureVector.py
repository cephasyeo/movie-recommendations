""" concatenate all features of movie into single feature vector """

import pandas as pd
import ast

def concatenate_embeddings(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    # convert string to lists as embeddings are in string
    def str_to_list(embedding):
        return ast.literal_eval(embedding) if isinstance(embedding, str) else embedding

    # concatenate embeddings into a single feature vector
    def create_movie_embeddings(row):
        genre_embeddings = str_to_list(row['genre_embeddings'])
        actor_embeddings = str_to_list(row['actor_embeddings'])
        director_embeddings = str_to_list(row['director_embeddings'])

        movie_feature_embeddings = genre_embeddings + actor_embeddings + director_embeddings

        return movie_feature_embeddings
    
    df['movie_embeddings'] = df.apply(create_movie_embeddings, axis = 1)

    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved as {output_csv}")

input_csv = "cleaned_train_set.csv"
output_csv = "train_wo_userprofile.csv"
concatenate_embeddings(input_csv, output_csv)