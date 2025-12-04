# Pine Tree Analyzer

A small but flexible Python toolset for analyzing pine tree records from the **San Francisco Street Tree List** dataset ([https://data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq](https://data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq)).

The project provides multiple methods—using **regex**, **CSV iteration**, **pandas**, and **collections.Counter**—to reliably detect and count pine-related tree species, trees maintained by the SF DPW, and specific pine varieties such as **Monterey Pine**.

---

## 🚀 Features

* Search tree records using **fast regex matching**
* Read CSV line-by-line using Python’s built-in `csv` module
* Analyze species counts using **pandas**
* Generate species summaries with **Counter**
* Unified, consistent result formatting
* Modular functions designed for reuse in larger data pipelines

---

## 📂 Project Structure

```
.
├── search_pine.py         # Main analysis script
├── test.csv               # Dataset downloaded from data.sfgov.org
├── README.md              # Project documentation
└── requirements.txt       # Optional: dependencies for pandas
```

---

## 🧠 How It Works

### 1. **Regex-based full-text search**

Reads the entire CSV file as text and finds matches using compiled regex patterns.

### 2. **CSV row-by-row parsing**

Reads structured CSV rows via `csv.reader`, normalizes text, then applies lighter regex or string matching.

### 3. **Pandas-based analysis (optional)**

Loads the dataset into a DataFrame for robust filtering, cleanup, and summarization.

### 4. **Species frequency counting**

Extracts species names and aggregates counts with Python’s `collections.Counter`.

---

## 📦 Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### (Optional) Install dependencies

```bash
pip install pandas
```

---

## ▶️ Usage

### Run the main script:

```bash
python search_pine.py
```

You will see output similar to:

```
Using regex method:
--------------------
There are 823 pine trees, 120 of which are city maintained.
There are 305 Monterey Pines.

Using CSV+Regex method:
------------------------
There are 823 pine trees, 120 of which are city maintained.
There are 305 Monterey Pines.
```

---

## 🔧 Configuration

### Change the target CSV file

Inside `search_pine.py`:

```python
FILE_PATH = "test.csv"
```

### Adjust species definitions

Modify `PINE_SPECIES` or regex patterns depending on how you define “pine tree” (strict species list vs. substring search).

---

## 📊 Notes About the SF Dataset

The dataset contains species values in **qSpecies**, **qSpeciesCode**, and sometimes mixed formatting like:

* `"Monterey Pine"`
* `"MONTEREY PINE "`
* `"Pine - Monterey"`
* `"Monterey  Pine"`

For accuracy, this project normalizes data by:

* stripping whitespace
* lowering text
* removing quotes
* handling NaN values

This ensures consistent results across regex, csv, and pandas methods.

---

## 🧪 Testing With Real Data

The dataset is large and contains inconsistent formatting.
Each method may yield slightly different results if normalization differs.

To ensure accurate comparison:

* all methods use the **same species extraction logic**,
* the **same text cleaning**,
* and the **same matching criteria**.

---


