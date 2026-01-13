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
    """Raised when a filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes."""

    def __init__(self, op: Callable, value) -> None:
        """Construct an AttributeFilter from a binary predicate and a reference value."""
        self.op = op
        self.value = value

    def __call__(self, approach: CloseApproach) -> bool:
        """Return whether `approach` satisfies this filter."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach: CloseApproach):
        """Get an attribute of interest from a close approach."""
        raise UnsupportedCriterionError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


# ---- Concrete filters ----

class DateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.time.date() if approach.time else None


class StartDateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.time.date() if approach.time else None


class EndDateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.time.date() if approach.time else None


class DistanceFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.distance


class VelocityFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.velocity


class DiameterFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.neo.diameter if approach.neo else float('nan')


class HazardousFilter(AttributeFilter):
    @classmethod
    def get(cls, approach: CloseApproach):
        return approach.neo.hazardous if approach.neo else False


def create_filters(
    date=None, start_date=None, end_date=None,
    distance_min=None, distance_max=None,
    velocity_min=None, velocity_max=None,
    diameter_min=None, diameter_max=None,
    hazardous=None
) -> Sequence[AttributeFilter]:
    """Create a collection of filters from user-specified criteria.

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

    If `n` is 0 or None, don't limit the iterator at all.
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
