import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import csv

load_dotenv(override=True)

URI = os.getenv("URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


# Initialize Neo4j connection
def connect_to_neo4j(uri, username, password):
    print(f"Loaded URI={uri}, USERNAME={username}, PASSWORD={password[:2]}***")
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print('Connected to Neo4j database.')
        return driver
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
        return None

# Function to query directors and movies
def query_directors_and_movies(driver):
    with driver.session() as session:
        query = """
        MATCH (m:Movie)<-[:DIRECTED]-(d:Director)
        RETURN d.name AS director, m.title AS movie
        LIMIT 10
        """
        result = session.run(query)

        print("Directors and their Movies:")
        for record in result:
            print(f"Director: {record['director']}, Movie: {record['movie']}")

if __name__ == "__main__":
    driver = connect_to_neo4j(URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    if driver:
        query_directors_and_movies(driver)
        driver.close()