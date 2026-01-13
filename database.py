"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.

----------------------------------------------------------------------------

A database encapsulating collections of near-Earth objects and their close approaches.

NEODatabase links NEOs with their close approaches and provides fast lookups
by designation or name, plus a streaming query that yields matching approaches.
"""

from __future__ import annotations

from typing import Dict, Iterable, Iterator, List, Optional, Sequence

from models import NearEarthObject, CloseApproach


class NEODatabase:
    """A database of near-Earth objects and their close approaches."""

    def __init__(self, neos: Sequence[NearEarthObject], approaches: Sequence[CloseApproach]) -> None:
        """Create a new NEODatabase and link NEOs with their close approaches.

        Parameters
        ----------
        neos : Sequence[NearEarthObject]
            Collection of NEOs (unlinked).
        approaches : Sequence[CloseApproach]
            Collection of close approaches (unlinked, with '_designation' present).

        Notes
        -----
        After construction:
        - Each CloseApproach.neo references its matching NearEarthObject.
        - Each NearEarthObject.approaches contains its approaches.
        - Auxiliary indices are built for designation and name.
        """
        self._neos: List[NearEarthObject] = list(neos)
        self._approaches: List[CloseApproach] = list(approaches)

        # Auxiliary indices
        self._by_des: Dict[str, NearEarthObject] = {neo.designation: neo for neo in self._neos}
        self._by_name: Dict[str, NearEarthObject] = {neo.name: neo for neo in self._neos if neo.name}

        # Link approaches <-> neos
        for app in self._approaches:
            neo = self._by_des.get(app._designation)
            if neo:
                app.neo = neo
                neo.approaches.append(app)

    def get_neo_by_designation(self, designation: str) -> Optional[NearEarthObject]:
        """Find and return an NEO by its primary designation, else None."""
        return self._by_des.get(designation)

    def get_neo_by_name(self, name: str) -> Optional[NearEarthObject]:
        """Find and return an NEO by its name, else None."""
        return self._by_name.get(name)

    def query(self, filters: Sequence) -> Iterator[CloseApproach]:
        """Yield close approaches that satisfy *all* filters.

        Parameters
        ----------
        filters : Sequence[AttributeFilter]
            A collection of filter predicates.

        Yields
        ------
        CloseApproach
            Matching approaches, lazily (no precomputation of full result set).
        """
        for app in self._approaches:
            if all(f(app) for f in filters):
                yield app
