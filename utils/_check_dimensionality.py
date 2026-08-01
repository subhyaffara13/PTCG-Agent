
def _check_dimensionality(points, values):
    if len(points) > values.ndim:
        raise ValueError(
            f"There are {len(points)} point arrays, but values has "
            f"{values.ndim} dimensions"
        )
    for i, p in enumerate(points):
        if not np.asarray(p).ndim == 1:
            raise ValueError(f"The points in dimension {i} must be 1-dimensional")
        if not values.shape[i] == len(p):
            raise ValueError(
                f"There are {len(p)} points and {values.shape[i]} values in "
                f"dimension {i}"
            )

