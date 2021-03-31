
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    def __init__(self, **info):
        #"""Create a new `NearEarthObject`.

        #:param info: A dictionary of excess keyword arguments supplied to the constructor.
        #"""
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        try:
            self.designation = str(info.get("designation") or "")
        except:
            self.designation = ''
        try:
            self.name = info.get("name") or ""
        except:
            self.name = None
        try:
            self.diameter = float(info.get("diameter") or "nan")
        except:
            self.diameter = float("nan")
        try:
            self.hazardous = info.get("hazardous")
        except:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        #"""Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        #if self.name != (None or ""):
            #return self.designation + " ( " + self.name + " ) "
        #else:
            #return self.designation
        if self.name:
            return self.designation + " ( " + self.name + " ) "
        else:
            return self.designation


    def __str__(self):
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        if self.hazardous:
            return f"NEO {self.fullname} has a diameter of {self.diameter} km and is potentially hazardous."
        else:
            return f"NEO {self.fullname} has a diameter of {self.diameter} km and is not potentially hazardous."

    def __repr__(self):
        #"""Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        #"""Create a new `CloseApproach`.

        #:param info: A dictionary of excess keyword arguments supplied to the constructor.
        #"""
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        try:
            self._designation = str(info.get("designation") or "")
        except:
            self._designation = ''
        try:
            self.time = cd_to_datetime(info.get("time"))
        except:
            self.time = None  # TODO: Use the cd_to_datetime function for this attribute.
        try:
            self.distance = float(info.get("distance") or "")
        except:
            self.distance = 0.0
        try:
            self.velocity = float(info.get("velocity") or "")
        except:
            self.velocity = 0.0

        # Create an attribute for the referenced NEO, originally None.
        try:
            self.neo = info.get("neos")
        except:
            self.neo = None

    @property
    def time_str(self):
        dt = self.time
        # TODO: Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        # TODO: Use self.designation and self.name to build a fullname for this object.
        return datetime_to_str(dt)

    @property
    def fullname(self):

        if self.neo.name:
            return self.__designation + " ( " + self.neo.name + " ) "

        else:
            return self._designation 
    def __str__(self):
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"At {self.time_str}, {self.neo.fullname} approaches Earth at a distance of {self.distance} au and a velocity of {self.velocity} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
