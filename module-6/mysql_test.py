import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "127.0.0.1",
    "database": "movies"
}

try:
    # Connect to the database
    connection = mysql.connector.connect(**config)
    print("Connection successful!")
    cursor = connection.cursor()

    # Query to show tables
    cursor.execute("SHOW TABLES;")
    print("Tables in the database:")
    for table in cursor.fetchall():
        print(table)

    # Close connection
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")