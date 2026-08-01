
def _rounding_offset(direction):
    # Return 2-tuple of -/+ 1.0 or 0.0 approximately based on the direction vector.
    # We divide the unit circle in 8 equal slices oriented towards the cardinal
    # (N, E, S, W) and intermediate (NE, SE, SW, NW) directions. To each slice we
    # map one of the possible cases: -1, 0, +1 for either X and Y coordinate.
    # E.g. Return (+1.0, -1.0) if unit vector is oriented towards SE, or
    # (-1.0, 0.0) if it's pointing West, etc.
    uv = _unit_vector(direction)
    if not uv:
        return (0, 0)

    result = []
    for uv_component in uv:
        if -_UNIT_VECTOR_THRESHOLD <= uv_component < _UNIT_VECTOR_THRESHOLD:
            # unit vector component near 0: direction almost orthogonal to the
            # direction of the current axis, thus keep coordinate unchanged
            result.append(0)
        else:
            # nudge coord by +/- 1.0 in direction of unit vector
            result.append(copysign(1.0, uv_component))
    return tuple(result)

