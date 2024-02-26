"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
from helpers import to_abs_path

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path: str) -> list:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        neos: list = []

        for row in reader:
            neo = NearEarthObject(row['pdes'], row['name'], row['diameter'], True if row['pha'] == 'Y' else False)
            neos.append(neo)
            
    return neos


def load_approaches(cad_json_path: str) -> list:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, 'r') as f:
        rows = json.load(f)
        cas: list = []
        
        for record in rows['data']:
           ca = CloseApproach(time = record[3], distance=record[4], velocity=record[7], designation=record[0])
           cas.append(ca) 
        
        
    return cas
