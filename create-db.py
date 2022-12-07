import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    # Create a database connection to a SQLite database

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Successfully created the database!')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    db_name = input('What would you like to call this db: ')
    create_connection(db_name)