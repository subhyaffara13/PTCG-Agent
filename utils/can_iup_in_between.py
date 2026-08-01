
def can_iup_in_between(
    deltas: _DeltaSegment,
    coords: _PointSegment,
    i: Integral,
    j: Integral,
    tolerance: Real,
):  # -> bool:
    """Return true if the deltas for points at `i` and `j` (`i < j`) can be
    successfully used to interpolate deltas for points in between them within
    provided error tolerance."""

    assert j - i >= 2
    interp = iup_segment(coords[i + 1 : j], coords[i], deltas[i], coords[j], deltas[j])
    deltas = deltas[i + 1 : j]

    return all(
        abs(complex(x - p, y - q)) <= tolerance
        for (x, y), (p, q) in zip(deltas, interp)
    )

