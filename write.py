"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""



"""Write a stream of close approaches to CSV or to JSON."""

import csv
import json
from pathlib import Path
from typing import Iterable

from models import CloseApproach


def write_to_csv(results: Iterable[CloseApproach], filename: Path) -> None:
    """Write an iterable of CloseApproach objects to a CSV file.

    Output columns:
      datetime_utc, distance_au, velocity_km_s, designation, name, diameter_km, potentially_hazardous
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ca in results:
            writer.writerow(ca.to_csv_row())


def write_to_json(results: Iterable[CloseApproach], filename: Path) -> None:
    """Write an iterable of CloseApproach objects to a JSON file.

    Output structure: a list of dicts; each dict has approach fields and an 'neo' sub-dict.
    """
    payload = [ca.serialize() for ca in results]
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
