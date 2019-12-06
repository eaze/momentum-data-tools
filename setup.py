import os
import psycopg2

USERNAME = 'postgres'
DATABASE_NAME = 'postgres'
PORT = 5432
CONFIG_FILE_NAME = '.config'


def main():
    print("\n\n\nLet's setup your local machine to connect to your database\n")
    print("The first thing we need is the endpoint AWS provided you.\n")
    print("This should be a url that looks something like database-1.123456.us-east-1.rds.amazonaws.com\n\n")
    host = input("Copy and Paste your endpoint and hit enter.\n\n").strip()
    pw = input("Enter the password you selected for this database user. Note: this is different from your login.\n\n").strip()
    print("Attempting to connect to database . . .")
    conn = psycopg2.connect(
        database=DATABASE_NAME,
        user=USERNAME,
        password=pw,
        host=host,
        port=PORT,
        )
    print("Successfully connected to database\n")
    with open(os.path.join(os.getcwd(), CONFIG_FILE_NAME), 'w') as f:
        f.write(f"""user: {USERNAME}
password: {pw}
database: {DATABASE_NAME}
port: {PORT}
host: {host}""")
    print("Successfully saved credentials")


if __name__ == '__main__':
    main()
