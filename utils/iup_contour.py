
def iup_contour(deltas: _DeltaOrNoneSegment, coords: _PointSegment) -> _DeltaSegment:
    """For the contour given in `coords`, interpolate any missing
    delta values in delta vector `deltas`.

    Returns fully filled-out delta vector."""

    assert len(deltas) == len(coords)
    if None not in deltas:
        return deltas

    n = len(deltas)
    # indices of points with explicit deltas
    indices = [i for i, v in enumerate(deltas) if v is not None]
    if not indices:
        # All deltas are None.  Return 0,0 for all.
        return [(0, 0)] * n

    out = []
    it = iter(indices)
    start = next(it)
    if start != 0:
        # Initial segment that wraps around
        i1, i2, ri1, ri2 = 0, start, start, indices[-1]
        out.extend(
            iup_segment(
                coords[i1:i2], coords[ri1], deltas[ri1], coords[ri2], deltas[ri2]
            )
        )
    out.append(deltas[start])
    for end in it:
        if end - start > 1:
            i1, i2, ri1, ri2 = start + 1, end, start, end
            out.extend(
                iup_segment(
                    coords[i1:i2], coords[ri1], deltas[ri1], coords[ri2], deltas[ri2]
                )
            )
        out.append(deltas[end])
        start = end
    if start != n - 1:
        # Final segment that wraps around
        i1, i2, ri1, ri2 = start + 1, n, start, indices[0]
        out.extend(
            iup_segment(
                coords[i1:i2], coords[ri1], deltas[ri1], coords[ri2], deltas[ri2]
            )
        )

    assert len(deltas) == len(out), (len(deltas), len(out))
    return out

