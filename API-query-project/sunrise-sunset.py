import datetime
import json
from typing import Optional, Dict, Any

import requests


class SunInfo:
    """Fetch sunrise, sunset, and day length information from sunrise-sunset.org."""

    BASE_URL = "https://api.sunrise-sunset.org/json"

    def __init__(self, latitude: float, longitude: float, date_str: str = "today") -> None:
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.date = (
            datetime.date.today().strftime("%Y-%m-%d")
            if date_str.lower() == "today"
            else date_str
        )
        self.data = self._query_api()

    def _query_api(self) -> Optional[Dict[str, Any]]:
        """Query the API and return the parsed JSON response."""
        params = {
            "lat": self.latitude,
            "lng": self.longitude,
            "date": self.date,
            "formatted": 1,
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                raise ValueError(f"API error: {data.get('status')}")

            return data["results"]

        except Exception as exc:
            print(f"Failed to retrieve data: {exc}")
            return None

    def get_sunrise(self) -> Optional[str]:
        return self.data.get("sunrise") if self.data else None

    def get_sunset(self) -> Optional[str]:
        return self.data.get("sunset") if self.data else None

    def get_day_length(self) -> Optional[str]:
        return self.data.get("day_length") if self.data else None


def main() -> None:
    """Command line interface for the SunInfo utility."""

    while True:
        latitude = input("Enter the latitude: ").strip()
        longitude = input("Enter the longitude: ").strip()
        date_str = input("Enter the date (YYYY-MM-DD) or 'today': ").strip()

        suninfo = SunInfo(latitude, longitude, date_str)

        print("\n--- Sun Information ---")
        print(f"Latitude:  {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Date:      {suninfo.date}")

        sunrise = suninfo.get_sunrise()
        sunset = suninfo.get_sunset()
        day_length = suninfo.get_day_length()

        if sunrise:
            print(f"Sunrise (UTC): {sunrise}")
            print(f"Sunset  (UTC): {sunset}")
            print(f"Day Length:    {day_length}")
        else:
            print("Could not retrieve sun data for the given parameters.")

        again = input("\nWould you like to continue? (y/n): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    main()

