import pandas as pd
import ast

def check_and_clean_embeddings(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    def is_valid_list(embedding):
        try:
            # Check if it can be converted to a list
            embedding = embedding.strip() if isinstance(embedding, str) else embedding
            if isinstance(embedding, str):
                ast.literal_eval(embedding.replace(" ", ","))
            return True
        except Exception:
            return False

    def clean_embedding(embedding):
        # Fix space-separated embeddings
        embedding = embedding.strip() if isinstance(embedding, str) else embedding
        return embedding.replace(" ", ",") if isinstance(embedding, str) else embedding

    # Check for invalid rows
    invalid_rows = df[
        (~df['genre_embeddings'].apply(is_valid_list)) |
        (~df['actor_embeddings'].apply(is_valid_list)) |
        (~df['director_embeddings'].apply(is_valid_list))
    ]

    if not invalid_rows.empty:
        print("Invalid rows found:")
        print(invalid_rows)
        invalid_rows.to_csv("invalid_rows.csv", index=False)

    # Clean the embeddings columns
    df['genre_embeddings'] = df['genre_embeddings'].apply(clean_embedding)
    df['actor_embeddings'] = df['actor_embeddings'].apply(clean_embedding)
    df['director_embeddings'] = df['director_embeddings'].apply(clean_embedding)

    # Save the cleaned dataset
    df.to_csv(output_csv, index=False)
    print(f"Cleaned CSV saved as {output_csv}")

# Input and output file paths
input_csv = "training_data/val_set.csv"
output_csv = "val_set.csv"

check_and_clean_embeddings(input_csv, output_csv)
