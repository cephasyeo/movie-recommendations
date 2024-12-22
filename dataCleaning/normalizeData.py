# normalize ratings and embeddings for persons
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

def normalize_ratings(csv_file_path, ratings_column_name, output_csv_path):
    df = pd.read_csv(csv_file_path)
    column_data = df[ratings_column_name]

    # min-max normalization
    scaler = MinMaxScaler()
    normalized_column = scaler.fit_transform(column_data.values.reshape(-1, 1))

    df[ratings_column_name] = normalized_column

    df.to_csv(output_csv_path, index=False)

    print(f"Normalized ratings saved to {output_csv_path}")

''' generate embeddings for all genres and names '''
# load pre-trained glove embeddings
def load_glove_embeddings(glove_file_path):
    embeddings = {}
    with open(glove_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype=np.float32)
            embeddings[word] = vector
    print(f"Loaded {len(embeddings)} GloVe embeddings.")
    return embeddings

# function to get embedding for a name (actor, director, or genre)
def get_embedding_for_name(name, glove_embeddings, embedding_dim=100):
    words = name.lower().split()
    vectors = []

    # try to find the embedding for each word in the name
    for word in words:
        if word in glove_embeddings:
            vectors.append(glove_embeddings[word])
        else:
            # if the word is not in GloVe, use a zero vector
            vectors.append(np.zeros(embedding_dim))

    if len(vectors) == 0:
        return np.zeros(embedding_dim) # return a zero vector if no embeddings are found

    # return the average of all word vectors for the name
    return np.mean(vectors, axis=0)

# func to process CSV data
def process_data_and_generate_embeddings(input_csv_path, glove_file_path, output_csv_path, embedding_dim=100):
    # Load CSV
    df = pd.read_csv(input_csv_path)
    glove_embeddings = load_glove_embeddings(glove_file_path)

    # Generate embeddings for genres, actors, and directors
    all_genre_embeddings = []
    all_actor_embeddings = []
    all_director_embeddings = []

    for _, row in df.iterrows():
        # Extract columns
        genres = eval(row['genres'])  # Convert string to list
        actors = eval(row['actors'])  # Convert string to list
        directors = eval(row['directors'])  # Convert string to list

        # Generate embeddings
        genre_embeddings = [get_embedding_for_name(genre, glove_embeddings, embedding_dim) for genre in genres]
        actor_embeddings = [get_embedding_for_name(actor, glove_embeddings, embedding_dim) for actor in actors]
        director_embeddings = [get_embedding_for_name(director, glove_embeddings, embedding_dim) for director in directors]

        # Average the embeddings for the group
        avg_genre_embedding = np.mean(genre_embeddings, axis=0) if genre_embeddings else np.zeros(embedding_dim)
        avg_actor_embedding = np.mean(actor_embeddings, axis=0) if actor_embeddings else np.zeros(embedding_dim)
        avg_director_embedding = np.mean(director_embeddings, axis=0) if director_embeddings else np.zeros(embedding_dim)

        # Append averaged embeddings to lists
        all_genre_embeddings.append(avg_genre_embedding)
        all_actor_embeddings.append(avg_actor_embedding)
        all_director_embeddings.append(avg_director_embedding)

    # Add embeddings back to the DataFrame as flattened strings
    df['genre_embeddings'] = [' '.join(map(str, emb)) for emb in all_genre_embeddings]
    df['actor_embeddings'] = [' '.join(map(str, emb)) for emb in all_actor_embeddings]
    df['director_embeddings'] = [' '.join(map(str, emb)) for emb in all_director_embeddings]

    # Save updated DataFrame to new CSV
    df.to_csv(output_csv_path, index=False)
    print(f"Processed data with embeddings saved to {output_csv_path}")

if __name__ == "__main__":
    input_csv_path = "combined_data.csv"  # Path to your input CSV
    glove_file_path = "glove.6B.100d.txt"  # Path to GloVe embeddings file
    output_csv_path_normalized = "normalized_movies.csv"  # Path to save normalized ratings
    output_csv_path_embeddings = "combined_data_with_embeddings.csv"  # Path to save final output with embeddings

    # Normalize ratings
    ratings_column_name = "rating"
    df_normalized = normalize_ratings(input_csv_path, ratings_column_name, output_csv_path_normalized)

    # Process genres, actors, and directors to generate embeddings
    process_data_and_generate_embeddings(output_csv_path_normalized, glove_file_path, output_csv_path_embeddings)