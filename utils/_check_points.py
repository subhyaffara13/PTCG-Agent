
def _check_points(points):
    descending_dimensions = []
    grid = []
    for i, p in enumerate(points):
        # early make points float
        # see https://github.com/scipy/scipy/pull/17230
        p = np.asarray(p, dtype=float)
        if not np.all(p[1:] > p[:-1]):
            if np.all(p[1:] < p[:-1]):
                # input is descending, so make it ascending
                descending_dimensions.append(i)
                p = np.flip(p)
            else:
                raise ValueError(
                    f"The points in dimension {i} must be strictly ascending or "
                    f"descending"
                )
        # see https://github.com/scipy/scipy/issues/17716
        p = np.ascontiguousarray(p)
        grid.append(p)
    return tuple(grid), tuple(descending_dimensions)

