import csv
import re
from collections import Counter
import pandas as pd

# ------------------------------
# Implementation 1: re.findall
# ------------------------------
def searchPine_findall(file_path):
    with open(file_path, newline='', encoding="utf-8") as f:
        text = f.read().replace('"', '')

    pattern_pine = re.compile(r'\d{5,6},.*?,.*\s[Pp]ine[,\s]')
    pattern_city_maintained_pine = re.compile(r'\d+,\s*DPW Maintained\s*,.*\s[Pp]ine[,\s]')
    pattern_Monterey_pine = re.compile(r'\d+,.*?,.*\sMonterey Pine[,\s]')

    total = len(pattern_pine.findall(text))
    DPW = len(pattern_city_maintained_pine.findall(text))
    monterey_count = len(pattern_Monterey_pine.findall(text))

    return total, DPW, monterey_count

# ------------------------------
# Implementation 2: csv.reader + regex
# ------------------------------
def searchPine_csv_regex(file_path):
    pine = Counter()
    total = DPW = 0

    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        pattern_pine = re.compile(r'\d+,(.*?),(.*\s[Pp]ine)\b')

        for row in reader:
            line = ",".join(row)
            match = pattern_pine.search(line)
            if match:
                total += 1
                if match.group(1).strip() == 'DPW Maintained':
                    DPW += 1
                tree = match.group(2).strip().split(':')[-1].strip()
                pine[tree] += 1

    monterey_count = pine.get("Monterey Pine", 0)
    return total, DPW, monterey_count

# ------------------------------
# Implementation 3: pandas
# ------------------------------
def searchPine_pandas(file_path):
    df = pd.read_csv(file_path, dtype=str)
    total = df[df.iloc[:, 2].str.contains(r'[Pp]ine', case=False)].shape[0]
    DPW = df[(df.iloc[:, 1].str.strip() == 'DPW Maintained') & df.iloc[:, 2].str.contains(r'[Pp]ine', case=False)].shape[0]
    monterey_count = df[df.iloc[:, 2].str.contains(r'\bMonterey Pine\b', na=False)].shape[0]
    return total, DPW, monterey_count



# Implementation 4: collections.Counter
# ------------------------------
def searchPine_counter(file_path):
    tree_counter = Counter()
    DPW = 0

    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
    for row in reader:
        tree_type = row[2].strip().split(":")[-1]
        owner = row[1].strip()
    if 'pine' in tree_type.lower():
        tree_counter[tree_type] += 1
    if owner == 'DPW Maintained':
        DPW += 1

    total = sum(tree_counter.values())
    monterey_count = tree_counter.get('Monterey Pine', 0)
    return total, DPW, monterey_count



# ------------------------------
# Helper function: print results
# ------------------------------
def print_info(total, DPW, monterey_count):
    print(f"Total pine trees: {total}")
    print(f"DPW Maintained: {DPW}")
    print(f"Monterey Pine: {monterey_count}")
    print("_"*40)

# ------------------------------
# Main CLI
# ------------------------------
def main():
    file_path = "test.csv"  # adjust path as needed

    methods = {
        're.findall': searchPine_findall,
        'csv + regex': searchPine_csv_regex,
        'pandas': searchPine_pandas,
        'collections.Counter': searchPine_counter
    }

    for name, func in methods.items():
        try:
            total, DPW, monterey_count = func(file_path)
            print(f"Results using {name} method:")
            print_info(total, DPW, monterey_count)
        except Exception as e:
            print(f"Error in {name} method: {e}")

if __name__ == "__main__":
    main()
