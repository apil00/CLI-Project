import sqlite3
import csv


# git config --global user.name "Your Name"
# git config --global user.email "your email"

# git init
# git status => to check the status of the repository
# git diff => to check the changes made in the files
# git add .
# git commit -m "Initial commit"

###################
# 1. change the code
# 2. git add .
# 3. git commit -m "Your commit message"
# 4. git push
###################


def create_connection():
    try:
        con = sqlite3.connect('users.sqlite3')
        return con
    except Exception as e:
        print(f"Error connecting to database: {e}")

INPUT_STRING = """
Enter the option:
    1. Create Table
    2. DUMP users from csv INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users from users TABLE
    5. QUERY user by ID from users TABLE
    6. QUERY specified no. of records from users TABLE
    7. DELETE ALL USERS
    8. DELETE user by ID from users TABLE
    9. UPDATE USER
    10.PRESS ANY KEY TO EXIT
"""

def create_table(con):
    CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name char(50) NOT NULL,
        last_name char(50) NOT NULL,
        company_name char(50) NOT NULL,
        address char(100) NOT NULL,
        city char(50) NOT NULL,
        county char(50) NOT NULL,
        state char(50) NOT NULL,
        zip REAL NOT NULL,
        phone1 char(20) NOT NULL,
        phone2 char(20),
        email char(50) NOT NULL,
        web text
    );
    """
    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("Users table created successfully.")

def read_csv():
    users = []
    with open('sample_users.csv', 'r') as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))

    return users[1:]  # Skip header row

def insert_users(con, users):
    user_add_query = """
    INSERT INTO users 
    (
        first_name,
        last_name,
        company_name,
        address,
        city,
        county,
        state,
        zip,
        phone1,
        phone2,
        email,
        web
    )
    VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cur = con.cursor()
    cur.executemany(user_add_query, users)
    con.commit()
    print(f"{len(users)} users were added successfully.")

def select_all_users(con):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def select_user_by_id(con, user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    for user in users:
        print(user)

def select_specified_no_of_user(con, no_of_users):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users LIMIT ?", (no_of_users,))
    for user in users:
        print(user)

def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("All users deleted successfully.")

def delete_user_by_id(con, user_id):
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    con.commit()
    print(f"User with ID {user_id} deleted successfully.")

COLUMNS = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web"
)

def update_user_by_id(con, user_id, column_name, column_new_value):
    cur = con.cursor()
    update_query = f"UPDATE users SET {column_name} = ? WHERE id = ?"
    cur.execute(update_query, (column_new_value, user_id))
    con.commit()
    print(f"User with ID {user_id} updated successfully.")


def main():
    con = create_connection()
    user_input = input(INPUT_STRING)
    if user_input == '1':
        create_table(con)
    elif user_input == '2':
        users = read_csv()
        insert_users(con,users)
    elif user_input == '3':
        user_data = []
        for column in COLUMNS:
            column_value = input(f"Enter Your {column}:")
            user_data.append(column_value)
        insert_users(con, [tuple(user_data)])
    elif user_input == '4':
        select_all_users(con)
    elif user_input == '5':
        user_id = input("Enter user ID: ")
        if user_id.isnumeric():
            select_user_by_id(con, user_id)
    elif user_input == '6':
        no_of_users = input("Enter number of users to query: ")
        if no_of_users.isnumeric():
            select_specified_no_of_user(con, no_of_users)
    elif user_input == '7':
            confirm = input("Are you sure you want to delete all users? (y/n): ")
            if confirm.lower() == 'y':
                delete_users(con)
    elif user_input == '8':
        user_id = input("Enter user ID to delete: ")
        if user_id.isnumeric():
            delete_user_by_id(con, user_id)
    elif user_input == '9':
        user_id = input("Enter user ID to update: ")
        if user_id.isnumeric():
            column_name = input(f"Enter the column you want to edit.\nPlease make sure colummn is with in {COLUMNS}: ")
            if column_name in COLUMNS:
                column_new_value = input(f"Enter new value for {column_name}: ")
                update_user_by_id(con, user_id, column_name, column_new_value)
            else:
                print("Invalid column name.")
    elif user_input == '10':
        pass
    
        
main()