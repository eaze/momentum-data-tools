import db_util

UPDATE_TYPES = {
    '1': 'FULL UPDATE',
    '2': 'INSERT ONLY',
    '3': 'UPSERT (UPDATE AND INSERT)',
}


def main():
    table_name = input("Which table would you like to update?\n").strip()
    if not db_util.check_table_exists(table_name):
        raise Exception("You need to create the table first. run python create_table.py")
    print(f"Great! {table_name} already exists!")
    update_type = input("""Which type of update would you like to do?
1. Full Update - Delete all data currently in the table and replace with CSV
2. Insert Only - Keep all data currently in the table and additionally add CSV data
3. Upsert - Keep all data in the table, updating records that changed, and adding new data from CSV\n
""").strip()
    csv_file = input("Drag and Drop the CSV file here.").strip()
    confirm = input(f"""To Confirm, {table_name} will be updated as {UPDATE_TYPES[update_type]} using {csv_file}.
Proceed? (Y/N)""")
    if 'n' in confirm.lower():
        print("Canceling Update, re-run to try again.")
        return
    if update_type == '1':
        db_util.update_table(table_name, csv_file)
    elif update_type == '2':
        db_util.insert_table(table_name, csv_file)
    else:
        db_util.upsert_table(table_name, csv_file)


if __name__ == '__main__':
    main()