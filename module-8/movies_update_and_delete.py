import mysql.connector

# Function to display films
def show_films(cursor, label):
    """
    Displays the current contents of the film table with selected fields.
    """
    print(f"\n{label}")
    query = """
    SELECT film.film_name AS "Film Name",
           film.film_releaseDate AS "Release Year",
           film.film_runtime AS "Runtime",
           film.film_director AS "Director",
           genre.genre_name AS "Genre",
           studio.studio_name AS "Studio"
    FROM film
    INNER JOIN genre ON film.genre_id = genre.genre_id
    INNER JOIN studio ON film.studio_id = studio.studio_id;
    """
    cursor.execute(query)
    films = cursor.fetchall()
    for film in films:
        print(f"Film Name: {film[0]}, Release Year: {film[1]}, Runtime: {film[2]} mins, "
              f"Director: {film[3]}, Genre: {film[4]}, Studio: {film[5]}")

# Function to clear the database and reinsert default data, I was having duplicate movie titles pop up so I looked up how to add all this in and it seemed to work 
def reset_database(cursor):
    """
    Clears all data from the film, genre, and studio tables and reinserts default data.
    """
    try:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Truncate tables
        cursor.execute("TRUNCATE TABLE film;")
        cursor.execute("TRUNCATE TABLE genre;")
        cursor.execute("TRUNCATE TABLE studio;")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        # Insert default studios
        cursor.execute("INSERT INTO studio (studio_name) VALUES ('20th Century Fox');")
        cursor.execute("INSERT INTO studio (studio_name) VALUES ('Blumhouse Productions');")
        cursor.execute("INSERT INTO studio (studio_name) VALUES ('Universal Pictures');")
        
        # Insert default genres
        cursor.execute("INSERT INTO genre (genre_name) VALUES ('Horror');")
        cursor.execute("INSERT INTO genre (genre_name) VALUES ('SciFi');")
        cursor.execute("INSERT INTO genre (genre_name) VALUES ('Drama');")
        
        # Insert default films
        cursor.execute("""
            INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
            VALUES ('Gladiator', '2000', 155, 'Ridley Scott',
                    (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),
                    (SELECT genre_id FROM genre WHERE genre_name = 'Drama'));
        """)
        cursor.execute("""
            INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
            VALUES ('Alien', '1979', 117, 'Ridley Scott',
                    (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox'),
                    (SELECT genre_id FROM genre WHERE genre_name = 'SciFi'));
        """)
        cursor.execute("""
            INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
            VALUES ('Get Out', '2017', 104, 'Jordan Peele',
                    (SELECT studio_id FROM studio WHERE studio_name = 'Blumhouse Productions'),
                    (SELECT genre_id FROM genre WHERE genre_name = 'Horror'));
        """)
        print("Database reset with default data.")
    except mysql.connector.Error as err:
        print(f"Error resetting the database: {err}")

# Function to connect to the database
def connect_to_database():
    """
    Establishes a connection to the database.
    """
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="movies_user",
            password="popcorn",
            database="movies"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Main function
def main():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        # Reset the database and display initial films
        reset_database(cursor)
        connection.commit()
        show_films(cursor, "DISPLAYING FILMS")

        # Insert Inception
        try:
            insert_query = """
            INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
            SELECT %s, %s, %s, %s, 
                   (SELECT studio_id FROM studio WHERE studio_name = %s),
                   (SELECT genre_id FROM genre WHERE genre_name = %s)
            WHERE NOT EXISTS (
                SELECT 1 FROM film WHERE film_name = %s
            );
            """
            cursor.execute(insert_query, ("Inception", "2010", 148, "Christopher Nolan", "20th Century Fox", "SciFi", "Inception"))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting 'Inception': {err}")

        # Display films after insertion
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # Update the genre of the film "Alien"
        try:
            update_query = """
            UPDATE film
            SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
            WHERE film_name = 'Alien';
            """
            cursor.execute(update_query)
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating 'Alien': {err}")

        # Display films after update
        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

        # Delete the film "Gladiator"
        try:
            delete_query = "DELETE FROM film WHERE film_name = 'Gladiator';"
            cursor.execute(delete_query)
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting 'Gladiator': {err}")

        # Display films after deletion
        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

        # Close resources
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()