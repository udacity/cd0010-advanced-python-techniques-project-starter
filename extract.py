"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.

----------------------------------------------------------------------------

Extract data on near-Earth objects and close approaches from CSV and JSON files.

- load_neos: read NEOs from CSV and return a collection of NearEarthObject.
- load_approaches: read close approaches from JSON and return a collection of CloseApproach.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path: Path) -> List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    Parameters
    ----------
    neo_csv_path : Path
        Path to the CSV file containing near-Earth objects.

    Returns
    -------
    List[NearEarthObject]
        A list of NEO instances.
    """
    neos: List[NearEarthObject] = []
    with open(neo_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Keep only the fields we care about; ignore extraneous columns
            info = {
                "pdes": row.get("pdes"),
                "name": row.get("name"),
                "diameter": row.get("diameter"),
                "pha": row.get("pha"),
            }
            neos.append(NearEarthObject(**info))
    return neos


def load_approaches(cad_json_path: Path) -> List[CloseApproach]:
    """Read close approach data from a JSON file.

    The NASA CAD file uses a 'fields' header list and a 'data' body list of rows.
    We map indices for 'des', 'cd', 'dist', 'v_rel' and build CloseApproach objects.

    Parameters
    ----------
    cad_json_path : Path
        Path to the JSON file containing close approach data.

    Returns
    -------
    List[CloseApproach]
        A list of CloseApproach instances.
    """
    approaches: List[CloseApproach] = []
    with open(cad_json_path, mode="r", encoding="utf-8") as f:
        raw = json.load(f)

    fields = raw.get("fields", [])
    data_rows = raw.get("data", [])

    idx = {name: i for i, name in enumerate(fields)}
    # Expected field names in NASA CAD: 'des', 'cd', 'dist', 'v_rel'
    for row in data_rows:
        info = {
            "des": row[idx.get("des", -1)] if idx.get("des") is not None else None,
            "cd": row[idx.get("cd", -1)] if idx.get("cd") is not None else None,
            "dist": row[idx.get("dist", -1)] if idx.get("dist") is not None else None,
            "v_rel": row[idx.get("v_rel", -1)] if idx.get("v_rel") is not None else None,
        }
        approaches.append(CloseApproach(**info))
    return approaches
