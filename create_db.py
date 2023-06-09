import psycopg2
#from dotenv import load_dotenv, find_dotenv
import os

#load_dotenv(find_dotenv())


def create_db():
    global connection
    try:
        connection = psycopg2.connect(
            host=os.environ.get("HOST_DB"),
            user=os.environ.get("USER_DB"),
            password=os.environ.get("PASSWORD_DB"),
            database=os.environ.get("NAME_DB"),
            port=os.environ.get("PORT_DB")
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                password VARCHAR(256)
                );
            '''
                           )
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_mails (
            id SERIAL PRIMARY KEY,
            id_user INTEGER REFERENCES users(id),
            mail VARCHAR(100)
            );
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS letters (
            id SERIAL PRIMARY KEY,
            id_user_mail INTEGER REFERENCES user_mails(id),
            letter_text TEXT,
            checked BOOLEAN,
            get_date DATE,
            type BOOLEAN
            );
            ''')
    except Exception as _ex:
        print('Error while working with PostgreSQL\n', '-' * 50, '\n', _ex, '-' * 50)
    finally:
        if connection:
            connection.close()
            print('Connection closed')
