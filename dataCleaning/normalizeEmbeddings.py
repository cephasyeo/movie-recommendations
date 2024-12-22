''' normalize the embeddings for cosine similarity since i forgot to do it earlier'''
import pandas as pd
import numpy as np

def normalize_embeddings(row, column_name):
    """
    normalise the embeddings in the specified column of a row.
    args:
    - row: a row from the df
    - column_name: the name of column containing the embeddings
    returns:
    - a normalized embedding as a string
    """
    try:
        # convert the string of embeddings into a numpy array
        embeddings = np.array(list(map(float, row[column_name].split())))

        # normalize embeddings
        norm = np.linalg.norm(embeddings)
        if norm == 0:
            return row[column_name] # skip normalization if norm is 0 (which should be impossible)
        normalized_embeddings = embeddings / norm

        # convert back to string format
        return " ".join(map(str, normalized_embeddings))
    
    except Exception as e:
        print(f"Error normalizing row {row.name}: {e}")
        return row[column_name]
    
def normalize_csv(file_path, output_file, columns_to_normalize):
    """
    normalize embeddings in specified columns of a csv file
    args:
    - file_path: path to input csv file
    - output_file: path to save the normalized csv file
    - columns_to_normalize: list of columns containing the embeddings to normalize 
    """
    # load csv file
    df = pd.read_csv(file_path)

    # normalize each specified column
    for column in columns_to_normalize:
        if column in df.columns:
            df[column] = df.apply(lambda row: normalize_embeddings(row, column), axis = 1)
        else:
            print(f"Column '{column}' not found in the CSV.")
    
    # save updated df
    df.to_csv(output_file, index=False)

input_csv = "data\combined_data_with_embeddings.csv"
output_csv = "final_data.csv"
embedding_columns = ["genre_embeddings", "actor_embeddings", "director_embeddings"]
normalize_csv(input_csv, output_csv, embedding_columns)