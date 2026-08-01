
def Location(location: Mapping[str, float]) -> LocationTuple:
    """Create a hashable location from a dictionary-like location."""
    return tuple(sorted(location.items()))

