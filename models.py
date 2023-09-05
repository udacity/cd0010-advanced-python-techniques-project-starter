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
    
    """A near-Earth object (NEO)

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, designation, name, diameter = float('nan'), hazardous ='N'):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = designation
        self.name = name
        if self.name == '':
            self.name = None
        else:
            self.name = name
        self.diameter = diameter
        if not self.diameter:
            self.diameter = float('nan')
        else:
            self.diameter = float(diameter)
        self.hazardous = hazardous    
        if hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []
    

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        if self.name == None:
            self.full_name = f"{self.designation}"
        else:
            self.full_name = f"{self.designation}{self.name}"
        return self.fullname


    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"A NearEarthObject {self.name} has a diameter of {self.diameter:.3f} km" \
               f" and {'is' if self.hazardous else 'is not'} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f" diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    
    def __init__(self, _designation, time=cd_to_datetime, distance = float('nan'), velocity = float('nan')):
    
        self._designation = _designation
        self.time = time  # TODO: Use the cd_to_datetime function for this attribute.
        self.distance = distance
        if not distance:
            self.distance = float('nan')
        else: 
            self.distance = distance
        self.velocity = velocity
        if not velocity:
            self.velocity = float('nan')
        else:
            self.velocity = float(velocity)
        self.neo = None

    @property
    def time_str(self):

        return f"datetime_to_str={self.time}, designation={self._designation}, name={self.neo}"

  
    def __str__(self):
        """Return `str(self)`."""
        return f"A Close Approach at {self.time_str!r} by {self.neo!r} approaches at a distance of" \
               f"{self.distance:.2f} with a vecolity of {self.velocity:.2f} km/s."


    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
    

