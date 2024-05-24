import configparser
import pandas as pd
import pyodbc
import argparse
import time
import sqlModule as sm

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


def create_table_from_dataframe(conn, df, table_name):
    try:
        cursor = conn.cursor()
        # Drop table if already exit in the 
        cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}")
        # Generate SQL data type mappings based on DataFrame column types
        sql_data_types = {
            'int64': 'INT',
            'float64': 'FLOAT',
            'object': 'NVARCHAR(MAX)',
            'bool': 'BIT',
            'datetime64[ns]': 'DATETIME',
            'timedelta64[ns]': 'TIME',
            'category': 'NVARCHAR(MAX)'
        }
 
        # Generate SQL column definitions
        columns_sql = ', '.join([f'[{col}] {sql_data_types[str(df[col].dtype)]}' for col in df.columns])
 
        # Create the table
        create_table_sql = f"CREATE TABLE {table_name} ({columns_sql})"
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table created successfully based on DataFrame schema.")
    except pyodbc.Error as e:
        print(e)

def bulk_insert(conn, target_table, data_file, field_terminator=',', row_terminator='\n', batch_size=None, max_errors=None):
    try:
        cursor = conn.cursor()

        # Construct the BULK INSERT statement
        bulk_insert_query = f"""
            BULK INSERT {target_table}
            FROM '{data_file}'
            WITH (
                FIELDTERMINATOR = '{field_terminator}',
                ROWTERMINATOR = '{row_terminator}',
                FIRSTROW = 2
                {', BATCHSIZE = ' + str(batch_size) if batch_size is not None else ''}  -- Only add BATCHSIZE if not None
                {', MAXERRORS = ' + str(max_errors) if max_errors is not None else ''}  -- Only add MAXERRORS if not None
            )
        """

        # Execute the BULK INSERT statement
        cursor.execute(bulk_insert_query)    
         # Commit the transaction
        conn.commit()
        print("Data loaded from DataFrame to database successfully.")
    except pyodbc.Error as e:
        print(e)
        conn.rollback()




def read_data(conn,table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT TOP 10 * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except pyodbc.Error as e:
        print(e)

def delete_data(conn, id, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE pid=?", (id,))
        conn.commit()
        print("Data deleted successfully.")
    except pyodbc.Error as e:
        print(e)

def update_data(conn, id, table_name,column, new_value):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET {column}=? WHERE pid=?", (new_value, id))
        conn.commit()
        print("Data updated successfully.")
    except pyodbc.Error as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Database CRUD operations with age_gender movie data")
    parser.add_argument("--config-file", type=str, help="Config file containing database connection information")
    parser.add_argument("--csv-file", type=str, help="CSV file containing age_gender data")
    parser.add_argument("--read", action="store_true", help="Read data from the database")
    parser.add_argument("--update", nargs='+', type=str, help="Update data in the database (provide id, column, and new value)")
    parser.add_argument("--delete", type=int, help="Delete data from the database by id")
    parser.add_argument("--create-table", type=str, help="create table table-name")
    args = parser.parse_args()

    username = config.get('Settings','username')
    password = config.get('Settings','password')
    driver_name = config.get('Settings','DRIVER_NAME')
    database_name = config.get('Settings','DATABASE_NAME')
    server_name = config.get('Settings','SERVER_NAME')


    conn = create_connection(server_name, database_name, username, password)

    if conn is not None:
        table_name = args.create_table
        filepath = args.csv_file

        t_start_time = time.time()
        # read csv file into dataframe
        df = pd.read_csv(args.csv_file)
        
        # create table from dataframe
        start_time = time.time()
        create_table_from_dataframe(conn, df, table_name)
        time_taken = time.time()-start_time
        print("time_taken to create table" , time_taken)
        

        # bulk insertion of data into table
        start_time = time.time()
        bulk_insert(conn, table_name, filepath)
        time_taken = time.time()-start_time
        print("time_taken " , time_taken)

        print("total time_taken ", time.time()-t_start_time)
        
        if args.read:
            read_data(conn,table_name=table_name)

        if args.update:
            update_data(conn, args.update[0],table_name, args.update[1], args.update[2])

        if args.delete:
            delete_data(conn, args.delete,table_name)

        conn.close()
        print("Database connection closed.")

if __name__ == '__main__':
    main()