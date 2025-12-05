# San Francisco Tree Database (SQLite CLI Tool)

This project is a command-line tool for loading, querying, and managing a tree dataset using **SQLite**.  
It supports bulk CSV import, species lookup, address lookup, and full database resets.

The tool is designed to be simple, reliable, and easy to extend.  
All database operations are encapsulated inside a professional `TreeDatabase` class for clean structure and maintainability.

---

## Features

### ✔ Bulk load tree records from a CSV file  
Imports the first four CSV columns into the database:

- `ID`
- `Status`
- `Species`
- `Address`

### ✔ Query by species (case-insensitive substring search)  
Example: entering `"pine"` will match `"Monterey Pine"`, `"Pineapple Bush"`, etc.

### ✔ Query by address  
Search by any substring of the address field.

### ✔ Delete all records  
Quickly wipe the database and repopulate with new data.

### ✔ Clean, menu-driven CLI  
Simple numbered menu for all main actions.

### ✔ Professional code structure  
- Class-based database layer  
- Context managers for safe DB handling  
- Parameterized SQL queries  
- Safe identifier validation  
- Clear input validation and error messages  

---

## Requirements

- **Python 3.8+**
- No external dependencies (uses Python standard library: `sqlite3`, `csv`, `sys`, `re`)

---

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

### 2. Run the program

```bash
python trees.py
```

---

## Menu Options

When the program starts, it displays:

```
San Francisco Tree Database
1) Bulk read entries from a file
2) Delete all entries
3) Query by Species
4) Query by Address
5) Exit
```

---

## CSV Format

The input CSV must contain **at least four columns** in this order:

```
ID, Status, Species, Address, ...
```

All extra columns are ignored.

Example row:

```
12345, Alive, Monterey Pine, 500 Market Street
```

---

## Example Workflow

1. Choose **Option 1** and load a CSV file.  
2. Choose **Option 3** to search species.  
3. Enter `"oak"` or `"pine"` to find matching trees.  
4. Choose **Option 4** to search by partial address.  
5. Choose **Option 2** to clear the table.  
6. Choose **Option 5** to exit.

---

## Code Structure

```
trees.py
├── TreeDatabase class
│   ├── reset_table()
│   ├── bulk_insert()
│   ├── delete_all()
│   └── query_like()
├── load_menu()
├── print_records()
└── main()
```






