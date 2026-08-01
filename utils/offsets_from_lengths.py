
def offsets_from_lengths(list_of_points: list[cpy.PointArray]) -> cpy.OffsetArray:
    """Determine offsets from lengths of point arrays.
    """
    if not list_of_points:
        raise ValueError("Empty list passed to offsets_from_lengths")

    return np.cumsum([0] + [len(line) for line in list_of_points], dtype=offset_dtype)

