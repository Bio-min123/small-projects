# 🌳 Tree Searching System

A simple and user-friendly GUI application built with **Python Tkinter** that allows users  
to search tree information by **Tree ID** from the official *San Francisco Street Tree List* dataset.

This project demonstrates GUI design, CSV data processing, and user input validation in Python.

---

## 📌 Features

- 🔍 **Search by Tree ID**  
  Enter a unique tree ID and instantly display the tree's status, species, and address.

- 🖼 **Graphical User Interface**  
  Built with Tkinter for easy interaction and clean layout.

- ⚠️ **Input Checking & Validation**  
  Shows warnings if the Tree ID is not found.

- 📄 **Reads CSV Data**  
  Uses the “Street Tree List” dataset provided by the City of San Francisco.

---

## 📁 Project Structure

tree-search/
│
├── test.csv # Tree dataset
├── tree_gui.py # Main Tkinter GUI application
└── README.md # Documentation


---

## 🛠 Requirements

- **Python 3.8 or higher**
- Uses only built-in libraries:
  - `tkinter`
  - `csv`
  - `messagebox`
  - `re` (optional)

No additional installation or external packages required.

---

## ▶️ How to Run

1. Clone or download the project:
   ```bash
   git clone https://github.com/<yourname>/tree-search.git
   cd tree-search


Put the dataset in the same folder:

test.csv


Run the application:

python tree_gui.py


When the window opens:

Enter a Tree ID

Click Display Info

Tree details will appear at the bottom

📊 Example Output
✔ If a valid Tree ID is found:
Tree ID: 12345
Status: Alive
Species: Acer rubrum (Red Maple)
Address: 100 Main St, San Francisco, CA


📚 Dataset Source

San Francisco Street Tree List
Open Data Portal: https://data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq

The CSV used in this project was exported from this official dataset.

