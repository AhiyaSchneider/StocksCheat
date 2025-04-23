import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

class Database:
    def __init__(self, db_key):
        # Load environment variables from the .env file
        load_dotenv()

        # Determine the appropriate environment variable prefixes based on db_key
        if db_key == 'trump':
            prefix = 'DB_TRUMP_'
        elif db_key == 'elon':
            prefix = 'DB_ELON_'
        else:
            raise ValueError("Invalid db_key. Use 'trump' or 'elon'.")
        print(f'new db { db_key }')

        # Retrieve database connection details from environment variables
        db_host = os.getenv(f'{prefix}HOST')
        db_name = os.getenv(f'{prefix}NAME')
        db_user = os.getenv(f'{prefix}USER')
        db_password = os.getenv(f'{prefix}PASSWORD')

        # Establish the database connection
        self.connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        self.cursor = self.connection.cursor()

    def insert_post(self, post):
        insert_query = sql.SQL("""
            INSERT INTO posts (post_date, content, user_handle, source, stock_related, stock_name, influence)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
        self.cursor.execute(insert_query, (
            post['post_date'],
            post['content'],
            post['user_handle'],
            post['source'],
            post['stock_related'],
            post['stock_name'],
            post['influence']
        ))
        self.connection.commit()


    def close(self):
        self.cursor.close()
        self.connection.close()
