import sqlite3
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama for Windows Terminal colors
init(autoreset=True)

# Connect to SQLite database (acts like cloud storage)
conn = sqlite3.connect('cloud_database.db')
cursor = conn.cursor()

# Create a detailed table if it doesn’t exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT UNIQUE,
    address TEXT
)
''')
conn.commit()

# ========== Core Functions ==========

def add_user(name, email, phone, address):
    # Check for redundancy in email or phone
    cursor.execute("SELECT * FROM user_data WHERE email=? OR phone=?", (email, phone))
    existing = cursor.fetchone()

    if existing:
        print(Fore.RED + f"❌ Duplicate entry detected! Either email or phone already exists.")
        return False
    else:
        cursor.execute("INSERT INTO user_data (name, email, phone, address) VALUES (?, ?, ?, ?)", 
                       (name, email, phone, address))
        conn.commit()
        print(Fore.GREEN + f"✅ Data added successfully for {name}.")
        return True

def view_all_users():
    cursor.execute("SELECT id, name, email, phone, address FROM user_data")
    rows = cursor.fetchall()
    if not rows:
        print(Fore.YELLOW + "⚠️ No data found in the database.\n")
        return
    print(Fore.CYAN + "\n📦 Current Database Records:\n")
    print(tabulate(rows, headers=["ID", "Name", "Email", "Phone", "Address"], tablefmt="fancy_grid"))
    print("")

def delete_duplicate_entries():
    cursor.execute("""
        DELETE FROM user_data
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM user_data
            GROUP BY email, phone
        )
    """)
    conn.commit()
    print(Fore.GREEN + "🧹 All duplicate records removed successfully!")

def search_user(keyword):
    cursor.execute("""
        SELECT id, name, email, phone, address
        FROM user_data
        WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? OR address LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    if results:
        print(Fore.CYAN + f"\n🔍 Search results for '{keyword}':\n")
        print(tabulate(results, headers=["ID", "Name", "Email", "Phone", "Address"], tablefmt="fancy_grid"))
    else:
        print(Fore.YELLOW + f"⚠️ No records found for '{keyword}'.\n")

# ========== Main Program ==========
def main_menu():
    print(Fore.MAGENTA + Style.BRIGHT + "\n=== 🌩️ Data Redundancy Removal System (Cloud DB Simulation) ===\n")
    while True:
        print(Fore.BLUE + """
1️⃣  Add New User Data
2️⃣  View All Data
3️⃣  Remove Duplicate Data
4️⃣  Search Data
5️⃣  Exit
""")
        choice = input(Fore.WHITE + "Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            phone = input("Enter Phone: ")
            address = input("Enter Address: ")
            add_user(name, email, phone, address)

        elif choice == '2':
            view_all_users()

        elif choice == '3':
            delete_duplicate_entries()

        elif choice == '4':
            keyword = input("Enter keyword to search: ")
            search_user(keyword)

        elif choice == '5':
            print(Fore.CYAN + "👋 Exiting system. Have a great day!")
            break
        else:
            print(Fore.RED + "⚠️ Invalid choice! Please enter a number between 1-5.")

if __name__ == "__main__":
    main_menu()
