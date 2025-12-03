import os
from pathlib import Path
import argparse
from typing import Dict, List

# ------------------------------

# Implementation 1: Recursive

# ------------------------------

def search_recursive(path: str, min_size: int, found_files: Dict[str, int] = None) -> Dict[str, int]:
    """
    Recursively search for files larger than min_size.
    """
    if found_files is None:
        found_files = {}

    try:
        if os.path.isfile(path):
            size = os.path.getsize(path)
            if size >= min_size:
                found_files[path] = size
        elif os.path.isdir(path):
            for entry in os.listdir(path):
                search_recursive(os.path.join(path, entry), min_size, found_files)
    except PermissionError:
        pass  # skip files/directories without permission

    return found_files


# ------------------------------

# Implementation 2: Iterative using os.walk

# ------------------------------

def search_iterative(path: str, min_size: int) -> Dict[str, int]:
    """
    Iteratively search for files larger than min_size using os.walk.
    """
    found_files = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if os.path.getsize(filepath) >= min_size:
                    found_files[filepath] = os.path.getsize(filepath)
            except PermissionError:
                continue
    return found_files


# ------------------------------

# Implementation 3: Using pathlib

# ------------------------------

def search_pathlib(path: str, min_size: int) -> Dict[str, int]:
    """
    Search for files larger than min_size using pathlib.
    """
    found_files = {}
    p = Path(path)
    for f in p.rglob("*"):
        if f.is_file():
            try:
               if f.stat().st_size >= min_size:
                   found_files[str(f)] = f.stat().st_size
            except PermissionError:
               continue
    return found_files


# ------------------------------

# Helper function: Print results

# ------------------------------

def print_results(files: Dict[str, int], verbose: bool):
    print(f"{'Filename':<100}{'Size (bytes)':<20}")
    print("-" * 120)
    for f, size in files.items():
        print(f"{f:<100}{size:<20}")
    print(f"\nTotal files found: {len(files)}")


# ------------------------------

# Main CLI

# ------------------------------

def main():
    parser = argparse.ArgumentParser(description="Search for files larger than a given size.")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Directory path to start searching")
    parser.add_argument("min_size", type=float, help="Minimum file size in MB")
    parser.add_argument("-m", "--method", choices=["recursive", "iterative", "pathlib", "all"],
                        default="all", help="Search method to use")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    min_size_bytes = int(args.min_size * 1024 * 1024)

    methods = {
        "recursive": search_recursive,
        "iterative": search_iterative,
        "pathlib": search_pathlib
    }

    if args.method == "all":
        for name, func in methods.items():
            print(f"\n--- Using {name} method ---")
            files = func(args.path, min_size_bytes)
            print_results(files, args.verbose)
    else:
        func = methods[args.method]
        files = func(args.path, min_size_bytes)
        print_results(files, args.verbose)



if __name__ == "__main__":
    main()
