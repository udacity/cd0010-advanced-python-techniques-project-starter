"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field of
NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.

----------------------------------------------------------------------------

Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (UTC).
This module converts NASA calendar date strings to datetime, and vice versa.
"""

import datetime


def cd_to_datetime(calendar_date: str) -> datetime.datetime:
    """Convert a NASA-formatted calendar date/time description into a datetime.

    Expected NASA format example: '2020-Dec-31 12:00'.

    Notes
    -----
    Some datasets may use ISO-like 'YYYY-MM-DD HH:MM'. We try both.
    """
    if not calendar_date:
        return None  # type: ignore
    for fmt in ("%Y-%b-%d %H:%M", "%Y-%m-%d %H:%M"):
        try:
            return datetime.datetime.strptime(calendar_date, fmt)
        except ValueError:
            continue
    # If none matched, raise for visibility
    raise ValueError(f"Unsupported date format: {calendar_date!r}")


def datetime_to_str(dt: datetime.datetime) -> str:
    """Convert a naive Python datetime into a human-readable string (YYYY-MM-DD HH:MM)."""
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")
