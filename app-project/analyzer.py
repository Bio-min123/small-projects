import os
import numpy as np


def analyze(place: str, year: str) -> np.ndarray:
    file_path = os.path.join(os.getcwd(), "covid19cases_test.csv")
    columns_to_load = [0, 1, 10]  # date, area, positive_tests

    try:
        data = np.genfromtxt(
            file_path,
            delimiter=",",
            skip_header=1,
            usecols=columns_to_load,
            dtype=None,
            encoding="utf-8"
        )
    except OSError:
        print(f"[ERROR] File not found: {file_path}")
        return np.array([])

    if data.size == 0:
        return np.array([])

    place_mask = np.char.lower(data["f1"].astype(str)) == place.lower()

    if year.lower() == "all":
        final_mask = place_mask
    else:
        year_mask = np.char.find(data["f0"].astype(str), year) >= 0
        final_mask = place_mask & year_mask

    filtered = data[final_mask]

    if filtered.size == 0:
        return np.array([])

    try:
        return filtered["f2"].astype(float)
    except ValueError:
        print("[ERROR] Cannot convert positive test counts to float.")
        return np.array([])
