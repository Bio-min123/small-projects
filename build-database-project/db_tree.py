import sqlite3
import csv
import sys
import re


DBASE = "trees.db"
DTABLE = "trees"


# -----------------------------
# Utility: Safe SQL identifier check
# -----------------------------
def safe_identifier(name: str) -> str:
    """Validate SQL identifiers (table/column names)."""
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
        raise ValueError(f"Unsafe SQL identifier: {name}")
    return name


# -----------------------------
# Database class
# -----------------------------
class TreeDatabase:
    """Encapsulates all database operations for the tree database."""

    def __init__(self, db_path: str, table: str):
        self.db_path = db_path
        self.table = safe_identifier(table)

    def connect(self):
        """Return a new database connection."""
        return sqlite3.connect(self.db_path)

    def reset_table(self):
        """Drop and recreate the table."""
        with self.connect() as con:
            cur = con.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {self.table}")
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    ID      INTEGER PRIMARY KEY,
                    Status  TEXT,
                    Species TEXT,
                    Address TEXT
                )
            """)
            con.commit()

    def bulk_insert(self, filename: str) -> int:
        """Load CSV file into database, return number of entries added."""
        self.reset_table()

        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            rows = [row[0:4] for row in reader]

        with self.connect() as con:
            cur = con.cursor()
            cur.executemany(
                f"""
                INSERT INTO {self.table} (ID, Status, Species, Address)
                VALUES (?, ?, ?, ?)
                """,
                rows,
            )
            con.commit()

        return len(rows)

    def delete_all(self):
        """Delete all records from the table."""
        with self.connect() as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table}")
            con.commit()

    def query_like(self, column: str, keyword: str):
        """Perform LIKE query for a given column."""
        column = safe_identifier(column)

        pattern = f"%{keyword}%"
        sql = f"SELECT * FROM {self.table} WHERE {column} LIKE :pattern"

        with self.connect() as con:
            cur = con.cursor()
            cur.execute(sql, {"pattern": pattern})
            return cur.fetchall()


# -----------------------------
# UI Functions
# -----------------------------
def load_menu():
    print("\n" * 2)
    print("=== San Francisco Tree Database ===")
    print("1) Bulk read entries from a file")
    print("2) Delete all entries")
    print("3) Query by Species")
    print("4) Query by Address")
    print("5) Exit")

    while True:
        try:
            op = int(input("Enter your choice: ").strip())
            if op in (1, 2, 3, 4, 5):
                return op
            print("Invalid option. Please choose 1–5.")
        except ValueError:
            print("Please enter a valid number.")


def print_records(records):
    print("\n=== Query Results ===")
    print(f"Found {len(records)} matching record(s).")

    for row in records:
        print("-------------------------------")
        print(f"ID:      {row[0]}")
        print(f"Status:  {row[1]}")
        print(f"Species: {row[2]}")
        print(f"Address: {row[3]}")
    print("-------------------------------")


# -----------------------------
# Main logic
# -----------------------------
def main():
    db = TreeDatabase(DBASE, DTABLE)
    data_loaded = False

    while True:
        option = load_menu()

        if option == 1:
            filename = input("Enter CSV file path: ").strip()
            try:
                count = db.bulk_insert(filename)
                print(f"Successfully added {count} entries.")
                data_loaded = True
            except Exception as e:
                print(f"Error loading file: {e}")

        elif option == 2:
            if not data_loaded:
                print("Please load data first.")
                continue
            db.delete_all()
            print("All entries deleted.")

        elif option == 3:
            if not data_loaded:
                print("Please load data first.")
                continue
            species = input("Enter species keyword: ").strip()
            records = db.query_like("Species", species)
            print_records(records)

        elif option == 4:
            if not data_loaded:
                print("Please load data first.")
                continue
            address = input("Enter address keyword: ").strip()
            records = db.query_like("Address", address)
            print_records(records)

        elif option == 5:
            print("Exiting...")
            sys.exit()


if __name__ == "__main__":
    main()
