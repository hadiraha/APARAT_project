import mysql.connector
from dotenv import load_dotenv
import os


class Mysqlconnector:
    load_dotenv()
    DB_HOST = os.getenv('host')
    DB_USER = os.getenv('user')
    DB_PASS = os.getenv('pass')
    DB_NAME = os.getenv('database')
    DB_AUTH = os.getenv('auth_plugin')

    def __init__(self):
        self.conf = self.open_connection()        
        
    def open_connection(self):    
        try:
            config = mysql.connector.connect(host = self.DB_HOST, user = self.DB_USER, password = self.DB_PASS, auth_plugin = self.DB_AUTH)
            print("connecting to mysql was successfully")
            cursor = config.cursor() 
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}")
            cursor.execute(f"USE {self.DB_NAME}")
        except mysql.connector.Error as err:
            print(f'Error has just taken place --> {err}')
        return config
    
    def get_table_already_columns(self, tablename):
        cursor = self.conf.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {tablename}")
        columns = [column[0] for column in cursor.fetchall()]
        cursor.close()
        return columns

    def add_new_column(self, tablename, newcolumn):
        cursor = self.conf.cursor()
        query = f"ALTER TABLE {tablename} ADD {newcolumn} TEXT"
        cursor.execute(query)
        cursor.close()

    def create_table(self, tablename, data):
        cursor = self.conf.cursor()
        columns = ', '.join([f"{key} INT PRIMARY KEY" if key == 'id' else f"{key} TEXT" for key in data.keys()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {tablename} ({columns});"
        cursor.execute(create_table_query)
        self.conf.commit()
        cursor.close()

    def insert_value(self, tablename, data):
        ## Before inserting values we check if there is any new keys in JSON structcure over time:
        alredy_columns = self.get_table_already_columns(tablename)

        for key in data.keys():
            if key not in alredy_columns:
                self.add_new_column(tablename, key)

        cursor = self.conf.cursor()
        placeholders = ', '.join(['%s']*len(data))
        columns = ', '.join(data.keys())
        insert_values_query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_values_query, list(data.values()))
        self.conf.commit()
        cursor.close()

    def close_connection(self):
        if self.conf.is_connected():
            self.conf.close()
            print("connection got clossed")

# c = Mysqlconnector()

# c.close_connection()