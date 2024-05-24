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
 
def create_table_from_dataframe(conn, df, table_name):
    try:
        cursor = conn.cursor()

        # Drop the table if it exists
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_table_sql)

        # Generate SQL column definitions dynamically based on DataFrame column types
        columns_sql = ', '.join([f'[{col}] NVARCHAR(MAX)' for col in df.columns])

        create_table_sql = f"CREATE TABLE {table_name} ({columns_sql})"
        cursor.execute(create_table_sql)
        conn.commit()
        print(f"Table '{table_name}' created successfully based on DataFrame schema.")
    except pyodbc.Error as e:
        print(e)
 
def bulk_insert(conn, target_table, data_file, encoding='utf-8', field_terminator=',', row_terminator='\n', batch_size=None, max_errors=None):
    try:
        cursor = conn.cursor()
 
        bulk_insert_query = f"""
            BULK INSERT {target_table}
            FROM '{data_file}'
            WITH (
                DATAFILETYPE = 'char',
                CODEPAGE = '65001',  -- UTF-8 encoding
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
 

def main():
    parser = argparse.ArgumentParser(description="Database CRUD operations with age_gender movie data")
    parser.add_argument("--config-file", type=str, help="Config file containing database connection information")
    parser.add_argument("--csv-file", type=str, help="CSV file containing age_gender data")
    parser.add_argument("--create-table", type=str, help="create table table-name")
    args = parser.parse_args()
 
    df = pd.read_csv(args.csv_file, encoding='utf-8')
    username = config.get('Settings','username')
    password = config.get('Settings','password')
    driver_name = config.get('Settings','DRIVER_NAME')
    database_name = config.get('Settings','DATABASE_NAME')
    server_name = config.get('Settings','SERVER_NAME')
    conn = create_connection(server_name, database_name, username, password)
 
    if conn is not None:
        table_name = args.create_table
        create_table_from_dataframe(conn, df, table_name=table_name)
 
        if table_name in [x.table_name for x in conn.cursor().tables()]:
            start_time = time.time()
            print(args.csv_file)
            filepath = args.csv_file
            bulk_insert(conn, target_table=table_name, data_file=filepath)
 
            time_taken = time.time() - start_time
            print("time_taken ", time_taken)
        else:
            print(f"Table '{table_name}' was not created successfully. Aborting bulk insert.")
 
        conn.close()
        print("Database connection closed.")
 
if __name__ == '__main__':
    main()
