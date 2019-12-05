import psycopg2
import os


COL_TYPE_MAPPINGS = {
    '1': 'STRING',
    '2': 'INTEGER',
    '3': 'DECIMAL',
    '4': 'DATE',
    '5': 'TIMESTAMP',
}


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


def create_table(table, columns):
    conn_args = get_args()
    sql = get_create_table_text(table, columns)
    print(sql)
    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            print("Successfully Created Table")


def format_name(val):
    val = val.replace(' ', '_')
    val = val.lower()
    return val


def get_column_name():
    answer = input("What is the name of the column? \n(If this is the last column just hit enter)\n")
    if len(answer) == 0:
        return None
    else:
        return format_name(answer)


def get_column_type(col):
    answer = input(f"""What is the data type for {col}?
1. String - a sequence of characters (i.e., "jessica", "A234TH9012")
2. Integer - a whole number (i.e., 1 , 3234235)
3. Decimal - a number with a decimal point (i.e., 1.0, 5.64)
4. Date - a date without time - this must be formatted YYYY-MM-DD (i.e., '2019-01-01')
5. Timestamp - a date with time (i.e., 2019-01-01 12:35:15)

Please just enter the number. If you are unsure select 1.
""")
    if answer in COL_TYPE_MAPPINGS.keys():
        return COL_TYPE_MAPPINGS[answer]
    else:
        print("I'm sorry, that didn't make sense. Please answer again.")
        return get_column_type(col)


def main():
    table_name = format_name(input("What is the name of the table you would like to create?\n"))
    columns = []
    col_names = set()
    print("You can enter in column names one by one or upload a CSV for the names")
    answer = input("Would you like to get columns from a CSV? (Y/N)\n")
    if 'y' in answer.lower():
        pass
        # get column names from csv
    else:
        col = get_column_name()
        while col is not None:
            if col in col_names:
                print(f"I'm sorry, there is already a column named {col}. Please provide a unique column name.")
                col = get_column_name()
            else:
                col_names.add(col)
                col_type = get_column_type(col)
                is_primary_key = 'y' in input(f"Is {col} a primary key? (Y/N)\n").lower()
                columns.append({'name': col, 'type': col_type, 'is_primary_key': is_primary_key})
                col = get_column_name()
    col_string = '\n'.join([f"{x['name']} - {x['type']}" for x in columns])
    if len(columns) > 0:
        answer = input(f"""To confirm, you would like to create a table named {table_name} with the following Columns:
{col_string}
Is that Correct? (Y/N)
""")
        if 'y' in answer.lower():
            print("Great! I'm creating your table.")
            create_table(table_name, columns)
    else:
        print("Quitting process, re-run to start again.")
        return


if __name__ == '__main__':
    main()
