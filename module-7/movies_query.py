import mysql.connector

# Establish connection to the database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",          
            user="movies_user",      
            password="popcorn",  
            database="movies"          
        )
        if connection.is_connected():
            print("Connected to movies database!")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Execute and print query results
def execute_query(cursor, query, description):
    try:
        cursor.execute(query)
        print(description)
        results = cursor.fetchall()
        for row in results:
            print(row)
        print()  # Add a blank line for formatting
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")

# Main function
def main():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        # Query 1: Select all fields from the studio table
        query1 = "SELECT * FROM studio;"
        description1 = "Query 1: All fields from the studio table"
        execute_query(cursor, query1, description1)

        # Query 2: Select all fields from the genre table
        query2 = "SELECT * FROM genre;"
        description2 = "Query 2: All fields from the genre table"
        execute_query(cursor, query2, description2)

        # Query 3: Select film names with a runtime of less than 2 hours
        query3 = """
        SELECT film_name 
        FROM film 
        WHERE film_runtime < 120;
        """
        description3 = "Query 3: Movie names with runtime less than 2 hours"
        execute_query(cursor, query3, description3)

        # Query 4: List of film names and directors grouped by director
        query4 = """
        SELECT film_director, GROUP_CONCAT(film_name) AS films
        FROM film
        GROUP BY film_director;
        """
        description4 = "Query 4: List of film names and directors grouped by director"
        execute_query(cursor, query4, description4)

        # Close the connection
        cursor.close()
        connection.close()
        print("Database connection closed.")

# Run the script
if __name__ == "__main__":
    main()