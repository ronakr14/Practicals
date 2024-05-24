import configparser
import pandas as pd
import pyodbc
import argparse

config = configparser.ConfigParser()
config.read('config_1.ini')

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
        cursor.execute("IF OBJECT_ID('imdb', 'U') IS NOT NULL DROP TABLE imdb")
        column_types = {
            'Name': 'NVARCHAR(MAX)',
            'BirthYear': 'NVARCHAR(MAX)',
            'DeathYear': 'NVARCHAR(MAX)',
            'Profession': 'NVARCHAR(MAX)',
            'KnownForTitle': 'NVARCHAR(MAX)',
        }
        create_table_sql = f"CREATE TABLE imdb ({', '.join([f'{col} {col_type}' for col, col_type in column_types.items()])})"
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table created successfully based on DataFrame schema.")
    except pyodbc.Error as e:
        print(e)

def load_data(conn, df):
    try:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            row_values = [str(value) for value in row]
            cursor.execute("INSERT INTO imdb VALUES ({})".format(','.join('?' * len(row_values))), tuple(row_values))
        conn.commit()
        print("Data loaded from DataFrame to database successfully.")
    except pyodbc.Error as e:
        print(e)

def read_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imdb")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except pyodbc.Error as e:
        print(e)

def delete_data(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM imdb WHERE Name=?", (id,))
        conn.commit()
        print("Data deleted successfully.")
    except pyodbc.Error as e:
        print(e)

def update_data(conn, id, column, new_value):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE imdb SET {column}=? WHERE Name=?", (new_value, id))
        conn.commit()
        print("Data updated successfully.")
    except pyodbc.Error as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Database CRUD operations with imdb data")
    parser.add_argument("--config-file", type=str, help="Config file containing database connection information")
    parser.add_argument("--csv-file", type=str, help="CSV file containing imdb data")
    parser.add_argument("--read", action="store_true", help="Read data from the database")
    parser.add_argument("--update", nargs='+', type=str, help="Update data in the database (provide id, column, and new value)")
    parser.add_argument("--delete", type=str, help="Delete data from the database by id")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    username = config.get('Settings','username')
    password = config.get('Settings','password')
    driver_name = config.get('Settings','DRIVER_NAME')
    database_name = config.get('Settings','DATABASE_NAME')
    server_name = config.get('Settings','SERVER_NAME')
    conn = create_connection(server_name, database_name, username, password)
    if conn is not None:
       
       

        # if args.read:
        #     read_data(conn)

        if args.update:
            update_data(conn, args.update[0], args.update[1], args.update[2])

        if args.delete:
            delete_data(conn, args.delete)

        conn.close()
        print("Database connection closed.")

if __name__ == '__main__':
    main()