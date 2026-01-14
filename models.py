"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.

------------------------


This module defines two core data models:

- NearEarthObject (NEO): a near-Earth object with primary designation, optional
  name, optional diameter (km), and hazardous flag.
- CloseApproach: a close approach event with instant (UTC), distance (au),
  velocity (km/s), and a link to its NEO.

Docstring style: PEP 257 (module/class/function). See internal coding standards
for PEP 8 and PEP 257 references.

"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """Represent a near-Earth object (NEO).

    A NearEarthObject encapsulates semantic and physical parameters about the
    object, such as:
      - primary designation (string, required, unique),
      - IAU name (string or None),
      - diameter in kilometers (float, may be NaN if unknown),
      - hazardous flag (bool).

    It also maintains a collection of its close approaches that will be
    populated later by the NEODatabase constructor.
    """

    def __init__(self, **info: Any) -> None:
        """Create a new NearEarthObject.

        Parameters
        ----------
        info : dict
            Arbitrary mapping with keys from the CSV row. Expected keys include
            'pdes' (designation), 'name', 'diameter', 'pha'.

        Notes
        -----
        - Empty or missing `name` becomes None (we default to '' to safely call `.strip()`).
        - Unknown or invalid `diameter` becomes `float('nan')`.
        - `pha` is 'Y' or 'N'; coerced to bool (True only for 'Y').

        """
        # Primary designation: always present in dataset
        self.designation: str = (info.get('pdes') or info.get('designation') or '').strip()

        # Name may be empty or None in the dataset
        name_str = (info.get('name') or '').strip()
        # The 'name' field may be missing, None, or whitespace in source data.
        # Normalize to None when empty, and strip surrounding whitespace otherwise.
        # Avoid calling .strip() on None by defaulting to ''.
        self.name: Optional[str] = name_str or None

        # Diameter (km): may be missing or non-numeric -> NaN
        raw_diameter = info.get('diameter', '')
        try:
            self.diameter: float = float(raw_diameter) if str(raw_diameter).strip() != '' else math.nan
        except (TypeError, ValueError):
            self.diameter = math.nan

        # Potentially hazardous: NASA uses 'Y'/'N'
        pha = (info.get('pha') or info.get('hazardous') or '').strip()
        self.hazardous: bool = True if str(pha).upper() == 'Y' else False

        # Linked approaches are filled in by NEODatabase
        self.approaches: list[CloseApproach] = []

    @property
    def fullname(self) -> str:
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        diameter_txt = f"{self.diameter:.3f} km" if not math.isnan(self.diameter) else "unknown diameter"
        haz_txt = "is potentially hazardous" if self.hazardous else "is not potentially hazardous"
        return f"NEO {self.fullname} has {diameter_txt} and {haz_txt}."

    def __repr__(self) -> str:
        """Return a computer-readable string representation."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )

    def serialize(self) -> Dict[str, Any]:
        """Serialize the NEO into a dict suitable for JSON output."""
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """Represent a close approach to Earth by an NEO.

    A CloseApproach encapsulates the moment of closest approach (UTC), nominal
    distance in astronomical units, relative velocity in km/s, and a link to
    its NEO (populated later in NEODatabase).
    """

    def __init__(self, **info: Any) -> None:
        """Create a new CloseApproach.

        Parameters
        ----------
        info : dict
            Arbitrary mapping with keys from the JSON row. Expected keys include
            'des' (designation), 'cd' (calendar date string), 'dist' (au),
            'v_rel' (km/s).
        """
        self._designation: str = (info.get('des') or '').strip()

        # Time: parse via helpers; may be absent in malformed rows
        cd = info.get('cd')
        self.time = cd_to_datetime(cd) if cd else None

        # Distance & velocity: coerce to float with sensible defaults
        try:
            self.distance: float = float(info.get('dist', 0.0))
        except (TypeError, ValueError):
            self.distance = 0.0

        try:
            self.velocity: float = float(info.get('v_rel', 0.0))
        except (TypeError, ValueError):
            self.velocity = 0.0

        # Linked NEO reference; filled in by NEODatabase
        self.neo: Optional[NearEarthObject] = None

    @property
    def time_str(self) -> str:
        """Return a formatted representation of the approach time (YYYY-MM-DD HH:MM)."""
        return datetime_to_str(self.time) if self.time else ""

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        desig = self.neo.fullname if self.neo else self._designation or "<?>"
        return (
            f"On {self.time_str}, '{desig}' approaches Earth at a distance of "
            f"{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
        )

    def __repr__(self) -> str:
        """Return a computer-readable string representation."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def to_csv_row(self) -> Dict[str, Any]:
        """Return a flat dict row for CSV export."""
        neo = self.neo
        return {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
            "designation": (neo.designation if neo else self._designation),
            "name": (neo.name if neo else None),
            "diameter_km": (float("nan") if (not neo or math.isnan(neo.diameter)) else neo.diameter),
            "potentially_hazardous": (neo.hazardous if neo else False),
        }

    def serialize(self) -> Dict[str, Any]:
        """Return a nested dict ready for JSON export.

        Structure
        ---------
        {
        "datetime_utc": str,          # 'YYYY-MM-DD HH:MM' ('' si falta)
        "distance_au": float,
        "velocity_km_s": float,
        "neo": {
            "designation": str,
            "name": Optional[str],
            "diameter_km": float,       # float('nan') si desconocido
            "potentially_hazardous": bool
        }
        }

        Returns
        -------
        Dict[str, Any]
            JSON-serializable mapping of approach and NEO attributes.
        """
        neo = self.neo
        return {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
            "neo": (neo.serialize() if neo else {"designation": self._designation}),
        }
