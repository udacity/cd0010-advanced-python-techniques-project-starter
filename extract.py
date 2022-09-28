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
from typing import List

from models import NearEarthObject, CloseApproach

NEO_KEYS = {'pdes', 'name', 'diameter', 'pha'}


def load_neos(neo_csv_path: str) -> List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    near_earth_objects = []
    with open(neo_csv_path) as csv_file:
        neo_reader = csv.DictReader(csv_file)
        for row_dict in neo_reader:
            near_earth_objects.append(NearEarthObject(**{k: v for k, v in row_dict.items() if k in NEO_KEYS}))

    return near_earth_objects


def load_approaches(cad_json_path: str) -> List[CloseApproach]:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    close_approaches = []

    with open(cad_json_path) as json_data:
        data = json.load(json_data)
        fields = data['fields']
        dest_index = fields.index('des')
        time_index = fields.index('cd')
        dist_index = fields.index('dist')
        v_index = fields.index('v_rel')

        for row in data['data']:
            input_dict = {
                'des': row[dest_index],
                'cd': row[time_index],
                'dist': row[dist_index],
                'v_rel': row[v_index]
            }
            close_approaches.append(CloseApproach(**input_dict))

    return close_approaches
