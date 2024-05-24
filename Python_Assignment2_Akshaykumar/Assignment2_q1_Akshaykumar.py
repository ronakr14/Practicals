import configparser
import pandas as pd
import argparse
import pyodbc

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
        # Check if table exists, drop if it does
        cursor.execute("IF OBJECT_ID('Sales_Demo', 'U') IS NOT NULL DROP TABLE Sales_Demo")

        # Define column types based on DataFrame
        column_types = {
            'Region': 'NVARCHAR(MAX)',
            'Country': 'NVARCHAR(MAX)',
            'Item Type': 'NVARCHAR(MAX)',
            'Sales Channel': 'NVARCHAR(MAX)',
            'Order Priority': 'NVARCHAR(MAX)',
            'Order Date': 'NVARCHAR(MAX)',
            'Order ID': 'NVARCHAR(MAX)',
            'Ship Date': 'NVARCHAR(MAX)',
            'Units Sold': 'NVARCHAR(MAX)',
            'Unit Price': 'NVARCHAR(MAX)',
            'Unit Cost': 'NVARCHAR(MAX)',
            'Total Revenue': 'NVARCHAR(MAX)',
            'Total Cost': 'NVARCHAR(MAX)',
            'Total Profit': 'NVARCHAR(MAX)'
        }
        # Generate CREATE TABLE SQL statement
        create_table_sql = f"CREATE TABLE Sales_Demo ({', '.join([f'[{col}] {col_type}' for col, col_type in column_types.items()])})"
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
            cursor.execute("INSERT INTO Sales_Demo VALUES ({})".format(','.join('?' * len(row_values))), tuple(row_values))
        conn.commit()
        print("Data loaded from DataFrame to database successfully.")
    except pyodbc.Error as e:
        print(e)

def read_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sales_Demo")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except pyodbc.Error as e:
        print(e)

def delete_data(conn, ID):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Sales_Demo WHERE Order ID=?", (ID,))
        conn.commit()
        print("Data deleted successfully.")
    except pyodbc.Error as e:
        print(e)

def update_data(conn, id, column, new_value):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Sales_Demo SET [{column}]=? WHERE [Order ID]=?", (new_value, id))
        conn.commit()
        print("Data updated successfully.")
    except pyodbc.Error as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Database CRUD operations with Sales_Demo data")
    parser.add_argument("--config-file", type=str, help="Config file containing database connection information")
    parser.add_argument("--csv-file", type=str, help="CSV file containing Sales_Demo data")
    parser.add_argument("--read", action="store_true", help="Read data from the database")
    parser.add_argument("--update", nargs='+', type=str, help="Update data in the database (provide id, column, and new value)")
    parser.add_argument("--delete", type=int, help="Delete data from the database by id")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    server_name = config.get('Settings','SERVER_NAME')
    database_name = config.get('Settings','DATABASE_NAME')
    driver_name = config.get('Settings','DRIVER_NAME')
    username = config.get('Settings','username')
    password = config.get('Settings','password')
    conn = create_connection(server_name, database_name, username, password)
    if conn is not None:
        create_table_from_dataframe(conn, df)
        load_data(conn, df)

        if args.read:
            read_data(conn)

        if args.update:
            update_data(conn, args.update[0], args.update[1], args.update[2])

        if args.delete:
            delete_data(conn, args.delete)

        conn.close()
        print("Database connection closed.")

if __name__ == '__main__':
    main()
