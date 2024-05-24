import csv
import pyodbc
import argparse


def parse_config(config_file):
    """Parses the configuration file using argparse.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: A dictionary containing the parsed configuration values.
    """

    parser = argparse.ArgumentParser(description="Database CRUD operations with CSV import")
    parser.add_argument("--server", type=str, required=True, help="Server address")
    parser.add_argument("--database", type=str, required=True, help="Database name")
    parser.add_argument("--username", type=str, required=True, help="Username for database access")
    parser.add_argument("--password", type=str, required=True, help="Password for database access")
    parser.add_argument("--table", type=str, required=True, help="Table name for CRUD operations")
    parser.add_argument("--csv_file", type=str, required=True, help="Path to the CSV file")
    parser.add_argument("--encoding", type=str, default="utf-8", help="Encoding of the CSV file")
    parser.add_argument("--batch_size", type=int, default=1000, help="Number of rows to insert per batch")

    return parser.parse_args(config_file.split())  # Allow space-separated arguments


def connect_to_database(config):
    """Establishes a connection to the database.

    Args:
        config (dict): Configuration dictionary from argparse.

    Returns:
        pyodbc.Connection: A connection object to the database.
    """

    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']}"
    )
    return pyodbc.connect(conn_str)


def load_csv_data(csv_file, encoding):
    """Loads data from the CSV file into a list of dictionaries.

    Args:
        csv_file (str): Path to the CSV file.
        encoding (str): Encoding of the CSV file.

    Returns:
        list: A list of dictionaries representing the CSV data.
    """

    data = []
    with open(csv_file, "r", encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def insert_data(conn, table, data, batch_size):
    """Inserts data from the list into the database table in batches.

    Args:
        conn (pyodbc.Connection): Connection object to the database.
        table (str): Name of the table in the database.
        data (list): List of dictionaries representing the CSV data.
        batch_size (int): Number of rows to insert per batch.
    """

    cursor = conn.cursor()
    column_names = ", ".join(data[0].keys())
    placeholders = ", ".join(["?"] * len(data[0]))
    sql = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

    for i in range(0, len(data), batch_size):
        batch_data = data[i : i + batch_size]
        values = tuple([row.values() for row in batch_data])
        cursor.executemany(sql, values)

    conn.commit()


def main():
    """Parses configuration, connects to database, and performs CRUD operations."""

    config = parse_config(["config.txt"])  # Replace with your config file path
    conn = connect_to_database(config)

    try:
        csv_data = load_csv_data(config["csv_file"], config["encoding"])
        insert_data(conn, config["table"], csv_data, config["batch_size"])
        print("Data loaded successfully!")
    except (FileNotFoundError, pyodbc.Error) as e:
        print(f"An error occurred: {e}")
    # finally:
    #     conn.close()


if __name__ == "__main__":
    main()
