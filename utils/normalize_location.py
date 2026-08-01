
def normalizeLocation(
    location: Mapping[str, float],
    axes: Mapping[str, tuple[float, float, float]],
    extrapolate: bool = False,
    *,
    validate: bool = False,
) -> dict[str, float]:
    """Normalizes location based on axis min/default/max values from axes.

    >>> axes = {"wght": (100, 400, 900)}
    >>> normalizeLocation({"wght": 400}, axes)
    {'wght': 0.0}
    >>> normalizeLocation({"wght": 100}, axes)
    {'wght': -1.0}
    >>> normalizeLocation({"wght": 900}, axes)
    {'wght': 1.0}
    >>> normalizeLocation({"wght": 650}, axes)
    {'wght': 0.5}
    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 1.0}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': -1.0}
    >>> axes = {"wght": (0, 0, 1000)}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': 0.0}
    >>> normalizeLocation({"wght": -1}, axes)
    {'wght': 0.0}
    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 1.0}
    >>> normalizeLocation({"wght": 500}, axes)
    {'wght': 0.5}
    >>> normalizeLocation({"wght": 1001}, axes)
    {'wght': 1.0}
    >>> axes = {"wght": (0, 1000, 1000)}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': -1.0}
    >>> normalizeLocation({"wght": -1}, axes)
    {'wght': -1.0}
    >>> normalizeLocation({"wght": 500}, axes)
    {'wght': -0.5}
    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 0.0}
    >>> normalizeLocation({"wght": 1001}, axes)
    {'wght': 0.0}
    """
    if validate:
        assert set(location.keys()) <= set(axes.keys()), set(location.keys()) - set(
            axes.keys()
        )
    out = {}
    for tag, triple in axes.items():
        v = location.get(tag, triple[1])
        out[tag] = normalizeValue(v, triple, extrapolate=extrapolate)
    return out

