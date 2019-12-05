import os
import psycopg2


def get_args():
    args = {}
    with open(os.path.join(os.getcwd(), '.config'), 'r') as f:
        for line in f:
            l = line.split(':')
            args[l[0].strip()] = l[1].strip()
    return args


def get_create_table_text(table, columns):
    col_text = ",\n".join([f""" "{x['name']}" {x['type']} {'PRIMARY KEY' if x['is_primary_key'] else ''}""" for x in columns])
    sql = f"""CREATE TABLE {table} (
{col_text});
"""
    return sql


def get_upsert_text(table):
    sql = f"""SELECT column_name, is_nullable
FROM information_schema.columns
WHERE table_name = '{table}'
AND LOWER(is_nullable) = 'yes'
"""
    conn_args = get_args()
    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            columns = cursor.fetchall()
    update_text = '\n,'.join([f"{x[0]} = excluded.{x[0]}" for x in columns])
    column_list = ', '.join([f"{x[0]}" for x in columns])
    full_text = f"""CREATE TEMP TABLE temp_{table} LIKE {table};
COPY temp_{table} FROM STDIN With CSV;
INSERT INTO {table} ({column_list})
SELECT *
FROM temp_{table} ON CONFLICT
DO UPDATE SET {update_text}
"""
    return full_text


def create_table(table, columns):
    conn_args = get_args()
    sql = get_create_table_text(table, columns)
    print(f"Running query:\n {sql}")
    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            print("Successfully Created Table")

def update_table(table, csv_filename, full_update=True):
    conn_args = get_args()
    print("Connecting to Database . . .")
    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as cursor:
            with open(csv_filename, 'r') as f:
                if full_update:
                    print("Removing old data . . . ")
                    cursor.execute(f"TRUNCATE TABLE {table};")
                print(f"Copying data from {csv_filename}")
                cursor.copy_from(f, table)
                print(f"Successfully copied data into {table}")


def insert_table(table, data):
    update_table(table, csv_filename, full_update=False)


def upsert_table(table, data):
    conn_args = get_args()
    print("Connecting to Database . . .")
    copy_text = get_upsert_text(table)
    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as cursor:
            with open(csv_filename, 'r') as f:
                if full_update:
                    print("Removing old data . . . ")
                    cursor.execute(f"TRUNCATE TABLE {table};")
                print(f"Copying data from {csv_filename}")
                cursor.copy_from(f, table)
                print(f"Successfully copied data into {table}")

print(get_upsert_text('test_columns'))