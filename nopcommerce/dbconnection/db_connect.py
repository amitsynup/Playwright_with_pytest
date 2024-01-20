import mysql.connector
import json

def read_config():
    # Read configuration from config.json
    with open('/Users/synup/Desktop/Python /E_Commerce/nopcommerce/src/Testdata/config.json') as config_file:
        config_data = json.load(config_file)

    return config_data

def connect_to_db():
    # Read database configuration from config.json
    db_config = read_config().get("database", {})

    # Rename the keys to match mysql.connector.connect parameter names
    renamed_keys = {
        "db_user": "user",
        "db_password": "password",
        "db_host": "host",
        "db_name": "database"
    }

    for old_key, new_key in renamed_keys.items():
        if old_key in db_config:
            db_config[new_key] = db_config.pop(old_key)

    # Connect to the MySQL server
    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print(f"Connected to the '{db_config.get('database', '')}' database")

            # Create a cursor object to interact with the database
            cursor = connection.cursor()

            return connection, cursor

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return None, None

def execute_query(query):
    # Connect to the database and execute the query
    connection, cursor = connect_to_db()
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
