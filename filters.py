"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.

----------------------------------------------------------------------------

Provide filters for querying close approaches and limit the generated results.

- AttributeFilter: base class wrapping an operator and a reference value.
- Subclasses override `get(approach)` to return attribute to compare.
- create_filters: build a collection of filters from CLI args.
- limit: yield at most n values from an iterator (stream-safe).
"""

from __future__ import annotations

import operator
from typing import Callable, Iterable, Iterator, List, Optional, Sequence

from models import CloseApproach


class UnsupportedCriterionError(NotImplementedError):
    """Exception raised when a filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes."""

    def __init__(self, op: Callable, value) -> None:
        """Construct an AttributeFilter from a binary predicate and a reference value.

        Parameters
        ----------
        op : Callable
            A binary comparison operator (e.g., operator.eq, operator.ge).
        value : Any
            The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach: CloseApproach) -> bool:
        """Return whether the approach satisfies this filter.

        Parameters
        ----------
        approach : CloseApproach
            The close approach to evaluate.

        Returns
        -------
        bool
            True if the approach satisfies the filter criterion.
        """
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get an attribute of interest from a close approach.

        Parameters
        ----------
        approach : CloseApproach
            The close approach from which to extract an attribute.

        Returns
        -------
        Any
            The attribute value to be compared.

        Raises
        ------
        UnsupportedCriterionError
            This base implementation always raises this error.
        """
        raise UnsupportedCriterionError

    def __repr__(self) -> str:
        """Return a string representation of this AttributeFilter."""
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


# ---- Concrete filters ----

class DateFilter(AttributeFilter):
    """Filter close approaches by exact date."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the date from the approach's time.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        date or None
            The date of the approach, or None if time is missing.
        """
        return approach.time.date() if approach.time else None


class StartDateFilter(AttributeFilter):
    """Filter close approaches by start date (inclusive)."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the date from the approach's time.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        date or None
            The date of the approach, or None if time is missing.
        """
        return approach.time.date() if approach.time else None


class EndDateFilter(AttributeFilter):
    """Filter close approaches by end date (inclusive)."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the date from the approach's time.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        date or None
            The date of the approach, or None if time is missing.
        """
        return approach.time.date() if approach.time else None


class DistanceFilter(AttributeFilter):
    """Filter close approaches by distance."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the distance from the approach.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        float
            The distance in astronomical units.
        """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """Filter close approaches by velocity."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the velocity from the approach.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        float
            The velocity in km/s.
        """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Filter close approaches by NEO diameter."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the diameter from the approach's NEO.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        float
            The NEO's diameter in km, or NaN if unknown or NEO is missing.
        """
        return approach.neo.diameter if approach.neo else float('nan')


class HazardousFilter(AttributeFilter):
    """Filter close approaches by NEO hazardous status."""

    @classmethod
    def get(cls, approach: CloseApproach):
        """Extract the hazardous flag from the approach's NEO.

        Parameters
        ----------
        approach : CloseApproach
            The close approach.

        Returns
        -------
        bool
            True if the NEO is potentially hazardous, False otherwise.
        """
        return approach.neo.hazardous if approach.neo else False


def create_filters(
    date=None, start_date=None, end_date=None,
    distance_min=None, distance_max=None,
    velocity_min=None, velocity_max=None,
    diameter_min=None, diameter_max=None,
    hazardous=None
) -> Sequence[AttributeFilter]:
    """Create a collection of filters from user-specified criteria.

    Parameters
    ----------
    date : date, optional
        Filter by exact date.
    start_date : date, optional
        Filter by start date (inclusive).
    end_date : date, optional
        Filter by end date (inclusive).
    distance_min : float, optional
        Minimum distance in AU.
    distance_max : float, optional
        Maximum distance in AU.
    velocity_min : float, optional
        Minimum velocity in km/s.
    velocity_max : float, optional
        Maximum velocity in km/s.
    diameter_min : float, optional
        Minimum diameter in km.
    diameter_max : float, optional
        Maximum diameter in km.
    hazardous : bool, optional
        Filter by potentially hazardous status.

    Returns
    -------
    Sequence[AttributeFilter]
        Filters compatible with NEODatabase.query.
    """
    filters: List[AttributeFilter] = []

    if date is not None:
        filters.append(DateFilter(operator.eq, date))
    if start_date is not None:
        filters.append(StartDateFilter(operator.ge, start_date))
    if end_date is not None:
        filters.append(EndDateFilter(operator.le, end_date))

    if distance_min is not None:
        filters.append(DistanceFilter(operator.ge, float(distance_min)))
    if distance_max is not None:
        filters.append(DistanceFilter(operator.le, float(distance_max)))

    if velocity_min is not None:
        filters.append(VelocityFilter(operator.ge, float(velocity_min)))
    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, float(velocity_max)))

    if diameter_min is not None:
        filters.append(DiameterFilter(operator.ge, float(diameter_min)))
    if diameter_max is not None:
        filters.append(DiameterFilter(operator.le, float(diameter_max)))

    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, bool(hazardous)))

    return tuple(filters)


def limit(iterator: Iterable, n: Optional[int] = None) -> Iterator:
    """Produce a limited stream of values from an iterator.

    Parameters
    ----------
    iterator : Iterable
        The source iterator to limit.
    n : Optional[int], optional
        Maximum number of items to yield. If 0 or None, no limit is applied.

    Yields
    ------
    Any
        Items from the iterator, up to n items.

    Notes
    -----
    If n is 0 or None, don't limit the iterator at all.
    """
    if not n:
        # No limit: pass through
        for item in iterator:
            yield item
        return

    count = 0
    for item in iterator:
        if count >= n:
            break
        yield item
        count += 1
