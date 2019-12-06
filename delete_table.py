import db_util


def main():
    print("WARNING!! Deleting a table is permanent and you will not be able to recover data")
    table_name = input("Which table would you like to delete?\n").strip()
    if not db_util.check_table_exists(table_name):
        raise Exception(f"The table {table_name} does not exist.")
    confirm = input(f"""To Confirm, {table_name} will be deleted permanently. Proceed? (Y/N)""")
    if 'n' in confirm.lower():
        print("Canceling Deletion.")
        return
    db_util.delete_table(table_name)


if __name__ == '__main__':
    main()
