# SunInfo – Sunrise & Sunset Information Fetcher

SunInfo is a simple Python tool that retrieves **sunrise**, **sunset**, and **day-length** information for any latitude, longitude, and date using the public API from [sunrise-sunset.org](https://sunrise-sunset.org/api).

It provides:

* A `SunInfo` class for programmatic use
* A command-line interface for interactive input
* Automatic handling of “today”
* Clean API querying and JSON parsing

---

## Features

* Query sunrise, sunset, and total daylight duration
* Accepts any geographic coordinates
* Supports `"today"` or a specific date (`YYYY-MM-DD`)
* Graceful error handling on API failures
* Clean, easy-to-read implementation

---

## Requirements

The program uses Python 3 and the following libraries:

* `requests` (recommended)
* `datetime`
* `json`

If you cloned the version using `requests`, install it with:

```bash
pip install requests
```

---

## Usage

### Command-Line Mode

Run the script directly:

```bash
python suninfo.py
```

You will be prompted to enter:

* **Latitude**
* **Longitude**
* **Date** (`YYYY-MM-DD` or `today`)

Example:

```
Enter the latitude: 37.7749
Enter the longitude: -122.4194
Enter the date in YYYY-MM-DD format, or 'today': today

--- Sun Information ---
Latitude:  37.7749
Longitude: -122.4194
Date:      2025-12-08
Sunrise (UTC): 15:17:24 AM
Sunset  (UTC): 01:54:12 AM
Day Length:    10:36:48
```

---

## Programmatic Use

You can also import the `SunInfo` class into your own code:

```python
from suninfo import SunInfo

info = SunInfo(37.7749, -122.4194, "today")

print(info.get_sunrise())
print(info.get_sunset())
print(info.get_day_length())
```

---

## How It Works

1. The user inputs coordinates and a date.
2. The script contacts the Sunrise-Sunset API with parameters:

   * `lat`
   * `lng`
   * `date`
   * `formatted=1`
3. The API returns a JSON response containing sunrise, sunset, and day length.
4. The results are displayed in UTC time.

---
