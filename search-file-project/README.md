### 1. **search-file-project**

A tool that scans directories and reports files larger than a given size.
Includes **three implementations** to demonstrate different techniques in Python:

| Method    | Description                                         |
| --------- | --------------------------------------------------- |
| Recursive | Manual recursion using `os.listdir`                 |
| Iterative | Directory walking using `os.walk`                   |
| Pathlib   | Cleaner object-oriented approach using `Path.rglob` |

#### ⭐ Features

* Search using multiple algorithms
* Verbose and non-verbose output
* CLI interface using `argparse`
* Handles permission errors safely
* Cross-platform (Windows/macOS/Linux)

#### 🔧 Usage

Navigate to:

```
small-projects/search-file-project
```

Run:

```
python searchfile.py <path> <min_size_MB> [--method recursive|iterative|pathlib|all] [-v]
```

Examples:

```
python searchfile.py "C:\Users" 10
python searchfile.py "/home/user" 5 --method pathlib -v
python searchfile.py . 1 --method all
```

---

## 📚 Repository Structure

```
small-projects/
│
├── search-file-project/
│   ├── README.md
│   ├── src/ (optional future structure)
│   └── searchfile.py
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔍 Goals of This Repository

This repository serves as:

* A practice ground for writing **clean, maintainable Python**
* A showcase of **different implementation approaches** to the same problem
* A personal learning portfolio hosted on GitHub
* A foundation for future small projects (data processing, algorithms, tools, etc.)

---


## 🤝 Contributions

This repository is primarily for personal learning, but contributions, suggestions, and improvements are always welcome.
Feel free to open issues or submit pull requests.

---

## ⭐ Support

If you find these projects useful, please consider starring the repo!
It helps others find the project and motivates further development.

---
