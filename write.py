"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from typing import List

from models import CloseApproach


def write_to_csv(results: List[CloseApproach], filename: str) -> None:
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    # TODO: Write the results to a CSV file, following the specification in the instructions.
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow({
                'datetime_utc': result.time,
                'distance_au': result.distance,
                'velocity_km_s': result.velocity,
                'designation': result.designation,
                'name': result.neo.name,
                'diameter_km': result.neo.diameter,
                'potentially_hazardous': result.neo.hazardous
            })


def write_to_json(results: List[CloseApproach], filename: str) -> None:
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.
    json_output = []
    for result in results:
        json_output.append(
            {
                'datetime_utc': result.time_str,
                'distance_au': result.distance,
                'velocity_km_s': result.velocity,
                'neo': {
                    'designation': result.designation,
                    'name': result.neo.name,
                    'diameter_km': result.neo.diameter,
                    'potentially_hazardous': result.neo.hazardous
                }
            }
        )
    with open(filename, 'w') as json_file:
        json.dump(json_output, json_file)
