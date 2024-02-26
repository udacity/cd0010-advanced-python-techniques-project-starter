"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from models import NearEarthObject, CloseApproach


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos: list[NearEarthObject], approaches: list[CloseApproach]):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # TODO: What additional auxiliary data structures will be useful?

        # TODO: Link together the NEOs and their close approaches.
        # for neo in neos:
        #     neo.approaches = []
        #     for approach in approaches:
        #         if neo.designation == approach._designation:
        #             approach.neo = neo
        #             neo.approaches.append(approach)
        self.populate_relationships_single_pass(self._neos, self._approaches)

    def get_neo_by_designation(self, designation: str) -> NearEarthObject | None:
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        for neo in self._neos:
            if designation.strip().lower() == neo.designation.strip().lower():
                return neo
        return None

    def get_neo_by_name(self, name: str) -> NearEarthObject | None:
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos:
            if neo.name is None:
                continue

            if name.strip().lower() == neo.name.strip().lower():
                return neo
        return None

    def query(self, filters: set[str] = ()) -> CloseApproach:
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:

            yield approach

    def populate_relationships_single_pass(self, neos: list[NearEarthObject], close_approaches: list[CloseApproach]):
        # Combine objects from both lists into a single list with an additional flag
        combined_list = [
            (obj, True) if isinstance(obj, A)
            else (obj, False) for obj in neos + close_approaches
        ]

        # Iterate through the combined list
        for obj, is_a_close_approach in combined_list:
            if is_a_close_approach:
                # A object: update list_of_b
                for ca in close_approaches:
                    if ca._designation == obj.designation:
                        ca.neo = obj
                        obj.approaches.append(ca)
                else:
                    # B object: update object_a (using the flag to identify B objects)
                    if obj.neo in a_dict:
                        obj.neo = a_dict[obj.designation]
