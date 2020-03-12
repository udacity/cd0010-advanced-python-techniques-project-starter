class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.orbit_set = set()
        self.id = kwargs.get('id', None)
        if not self.id:
            raise Exception('No id for NEO!')
        self.name = kwargs.get('name', None)
        self.url = kwargs.get('nasa_jpl_url', None)
        self.hazardous = kwargs.get('is_potentially_hazardous_asteroid', None)
        self.min_diam_km = kwargs.get('estimated_diameter_min_kilometers', None)
        self.max_diam_km = kwargs.get('estimated_diameter_max_kilometers', None)


    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        self.orbit_set.add(orbit)

    def get_orbits(self):
        '''
        Returns the set of orbit objects
        '''
        return self.orbit_set


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.neo_set = set()
        self.close_date = None
        self.close_full_date = None
        self.miss_dist_km = None
        self.orbiting_body = None
        self.km_sec = None


