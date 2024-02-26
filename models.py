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
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation: str, name: str, diameter: str, hazardous: bool = False, close_approaches: list = None):
        if close_approaches is None:
            close_approaches = []
        """Create a new `NearEarthObject`.

        Args:
            designation (str): An NEO primary designation.
            name (str, optional): IAU name. Defaults to None.
            diameter (float, optional): Diameter in kilometers - sometimes unknown. Defaults to float('nan').
            hazardous (bool, optional): Potentially hazardous to Earth. Defaults to False.
            close_approaches (list, optional): A list of close approaches to Earth by this NEO. Defaults to {}.
        """
        self.designation = designation
        self.name = None if name == '' else name
        self.diameter = float('nan') if diameter == '' else float(diameter)
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = [] if close_approaches is None else close_approaches

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})"

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"{self.fullname} has a diameter of {self.diameter} km and {'is' if self.hazardous else 'is not'} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, time, distance: str, velocity: str, neo: NearEarthObject = None, designation: str = None) -> None:
        """Create a new `CloseApproach`.

        Args:
            time (str): Date and time of CA (in UTC).
            distance (str): The nominal approach distance in astronomical units (AU).
            velocity (str): The relative approach velocity in km/s.
            neo (NearEarthObject, optional): A near-Earth object. Defaults to None.
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        if neo is None:
            _designation = designation
        else:
            self.neo = neo

    @property
    def time_str(self) -> str:
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return str(datetime_to_str(self.time))

    def __str__(self) -> str:
        """Print a human-readable date and time of an NEO's approach with its distance and velocity.

        Returns:
            str: Approach information.
        """
        return f"On {self.time_str}, '{self.neo.fullname if self._designation is None else self._designation}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
