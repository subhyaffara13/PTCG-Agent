import functools

def _topmost_artist(
        artists,
        _cached_max=functools.partial(max, key=operator.attrgetter("zorder"))):
    """
    Get the topmost artist of a list.

    In case of a tie, return the *last* of the tied artists, as it will be
    drawn on top of the others. `max` returns the first maximum in case of
    ties, so we need to iterate over the list in reverse order.
    """
    return _cached_max(reversed(artists))

