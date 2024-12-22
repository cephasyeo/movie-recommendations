import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import csv

load_dotenv(override=True)

URI = os.getenv("URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# init neo4j connection
def connect_to_neo4j(uri, username, password):
    print(f"Loaded URI={URI}, USERNAME={NEO4J_USERNAME}, PASSWORD={NEO4J_PASSWORD[:2]}***")
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print('connected to neo4j db')
        return driver
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
        return None
    
# func to execute query and save results to csv file
def query_combined_data(driver, output_file):
    with driver.session() as session:
        # query to combine user interactions with movie metadata
        query = """
        MATCH (u:User)-[r:RATED]->(m:Movie)
        OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Actor)
        RETURN 
            u.userId AS userId, 
            m.movieId AS movieId, 
            r.rating AS rating, 
            m.title AS title, 
            COLLECT(DISTINCT g.name) AS genres, 
            COLLECT(DISTINCT d.name) AS directors, 
            COLLECT(DISTINCT a.name) AS actors
        """
        result = session.run(query)

        # extract field names
        field_names = result.keys()

        # write results to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(field_names)
            for record in result:
                writer.writerow([record[field] for field in field_names])
        print(f"Combined data saved to {output_file}")

if __name__ == "__main__":
    driver = connect_to_neo4j(URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    if driver:
            query_combined_data(driver, "combined_data.csv")

            driver.close()

