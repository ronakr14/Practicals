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


def create_table_from_dataframe(conn, df, table_name='Bikejourney'):
    try:
        cursor = conn.cursor()

        # Drop table if it exists
        cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}")

        # Infer column types based on DataFrame
        column_types = {col: 'NVARCHAR(MAX)' for col in df.columns}  # Default type as NVARCHAR(MAX)
        for col in df.columns:
            col_type = df[col].dtype
            if col_type == 'int64':
                column_types[col] = 'INT'
            elif col_type == 'float64':
                column_types[col] = 'FLOAT'
            elif col_type == 'datetime64[ns]':
                column_types[col] = 'DATETIME'
        
        # Generate CREATE TABLE SQL statement
        create_table_sql = f"CREATE TABLE {table_name} ({', '.join([f'[{col}] {col_type}' for col, col_type in column_types.items()])})"
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table created successfully based on DataFrame schema.")
    except pyodbc.Error as e:
        print("Error creating table:", e)

def load_data(conn, df):
    try:
        cursor = conn.cursor()
        data = df.values.tolist()

        # Prepare the SQL statement for bulk insertion
        sql_statement = "INSERT INTO Bikejourney VALUES ({})".format(','.join(['?'] * len(df.columns)))

        # Execute the SQL statement for bulk insertion
        cursor.executemany(sql_statement, data)

        # Commit the transaction
        conn.commit()

        print("Data loaded from DataFrame to database successfully.")
    except Exception as e:
        print(e)

def read_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bikejourney")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except pyodbc.Error as e:
        print(e)

def delete_data(conn, Number):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bikejourney WHERE Number=?", (Number,))
        conn.commit()
        print("Data deleted successfully.")
    except pyodbc.Error as e:
        print(e)

def update_data(conn, id, column, new_value):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Bikejourney SET [{column}]=? WHERE [Number]=?", (new_value, id))
        conn.commit()
        print("Data updated successfully.")
    except pyodbc.Error as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Database CRUD operations with BikeJourney data")
    parser.add_argument("--config-file", type=str, help="Config file containing database connection information")
    parser.add_argument("--csv-file", type=str, help="CSV file containing BikeJourney data")
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
            #read_data(conn)
            pass

        if args.update:
            update_data(conn, args.update[0], args.update[1], args.update[2])

        if args.delete:
            delete_data(conn, args.delete)

        conn.close()
        print("Database connection closed.")

if __name__ == '__main__':
    main()
