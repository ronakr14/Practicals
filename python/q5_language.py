import configparser
import pandas as pd
import pyodbc
import argparse
import time

config = configparser.ConfigParser()
config.read('config.ini')

def create_connection(server, database, username, password):
    conn = None
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                              ';DATABASE=' + database +
                              ';UID=' + username +
                              ';PWD=' + password)
        print("Database connection established.")
    except pyodbc.Error as e:
        print(e)
    return conn

def create_table_from_dataframe(conn, df):
    try:
        cursor = conn.cursor()
        cursor.execute("IF OBJECT_ID('words2', 'U') IS NOT NULL DROP TABLE words2")
        column_types = {col: 'NVARCHAR(MAX)' for col in df.columns}
        create_table_sql = f"CREATE TABLE words2 ({', '.join([f'{col} {col_type}' for col, col_type in column_types.items()])})"
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table created successfully based on DataFrame schema.")
    except pyodbc.Error as e:
        print(e)

def load_data(conn, df):
    try:
        cursor = conn.cursor()
        start_time = time.time()
        for _, row in df.iterrows():
            row_values = [str(value) for value in row]
            cursor.execute("INSERT INTO words2 VALUES ({})".format(','.join('?' * len(row_values))), tuple(row_values))
        conn.commit()
        end_time = time.time()
        print(f"Data loaded from DataFrame to database successfully. Time taken: {end_time - start_time:.2f} seconds")
    except pyodbc.Error as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Database CRUD operations with words data")
    parser.add_argument("--config-file", type=str, help="Config file containing database connection information")
    parser.add_argument("--csv-file", type=str, help="CSV file containing words data")
    parser.add_argument("--read", action="store_true", help="Read data from the database")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    username = config.get('Settings','username')
    password = config.get('Settings','password')
    driver_name = config.get('Settings','DRIVER_NAME')
    database_name = config.get('Settings','DATABASE_NAME')
    server_name = config.get('Settings','SERVER_NAME')
    conn = create_connection(server_name, database_name, username, password)
    if conn is not None:
        create_table_from_dataframe(conn, df)  
        load_data(conn, df)  

        conn.close()
        print("Database connection closed.")

if __name__ == '__main__':
    main()
