# Small Projects

A curated collection of small, self-contained Python projects designed for learning, experimentation, and practice. Each project focuses on a specific programming task such as file processing, search utilities, automation, or data handling.

---

Each subfolder contains one independent project and includes:

* Python source code
* A project-specific README
* Example usage (when applicable)

---

## 🔍 Featured Project: `search-file-project`

A recursive file-searching utility that scans directories, filters files by minimum size, and collects results.

### Functions

* **`search_recursive(path: str, min_size: int, found_files: Dict[str, int] | None) -> Dict[str, int]`**

  * Walks through directories
  * Checks file sizes
  * Returns a dictionary of matched files and their sizes

### Example usage

```bash
python searchfile.py --path "/some/folder" --min-size 5000
```

---

## 🛠 Requirements

* Python 3.10+
* Standard Library only (no external dependencies yet)

---

## 🚀 Usage

Clone the repository:

```bash
git clone https://github.com/Bio-min123/small-projects.git
cd small-projects
```

Navigate to any project and run the demo script.

---

## 📘 Roadmap

* Add more small projects
* Improve documentation consistency
* Publish examples and screenshots

---

