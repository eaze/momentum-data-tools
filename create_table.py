import csv

import db_util

COL_TYPE_MAPPINGS = {
    '1': 'VARCHAR',
    '2': 'INTEGER',
    '3': 'DECIMAL',
    '4': 'DATE',
    '5': 'TIMESTAMP',
}


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
1. Varchar / String - a sequence of characters (i.e., "jessica", "A234TH9012")
2. Integer - a whole number (i.e., 1 , 3234235)
3. Numeric / Float - a number with a decimal point (i.e., 1.0, 5.64)
4. Date - a date without time - this must be formatted YYYY-MM-DD (i.e., '2019-01-01')
5. Timestamp - a date with time (i.e., 2019-01-01 12:35:15)

Please just enter the number. If you are unsure select 1.
""")
    if answer in COL_TYPE_MAPPINGS.keys():
        return COL_TYPE_MAPPINGS[answer]
    else:
        print("I'm sorry, that didn't make sense. Please answer again.")
        return get_column_type(col)


def get_columns_from_csv():
    filename = input("Drag and drop the CSV here.\n").strip()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        column_names = next(reader)
        print(column_names)
    columns = []
    if len([x for x in column_names if len(x) == 0]) > 0:
        raise Exception('One or more columns does not have a name. Please fix your csv and try again.')
    if len(set(column_names)) != len(column_names):
        raise Exception('Column names must be unique. Please fix your csv and try again.')
    for col in column_names:
        col_type = get_column_type(col)
        is_primary_key = 'y' in input(f"Is {col} a primary key? (Y/N)\n").lower()
        columns.append({'name': col, 'type': col_type, 'is_primary_key': is_primary_key})
    return columns


def main():
    table_name = format_name(input("What is the name of the table you would like to create?\n"))
    columns = []
    col_names = set()
    print("You can enter in column names one by one or upload a CSV for the names")
    answer = input("Would you like to get columns from a CSV? (Y/N)\n")
    if 'y' in answer.lower():
        columns = get_columns_from_csv()
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
            db_util.create_table(table_name, columns)
    else:
        print("Quitting process, re-run to start again.")
        return


if __name__ == '__main__':
    main()
