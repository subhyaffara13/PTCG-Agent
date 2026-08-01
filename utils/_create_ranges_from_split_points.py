
def _create_ranges_from_split_points(
    split_points: list[int],
) -> list[tuple[int, int] | tuple[int, float]]:
    """Convert split points into ranges for autotuning dispatch.

    Example:
        split_points=[512, 2048]
        returns:
               [(1, 512), (513, 2048), (2049, float('inf'))]
    """
    ranges: list[tuple[int, int] | tuple[int, float]] = []
    start = 1

    for split_point in split_points:
        ranges.append((start, split_point))
        start = split_point + 1

    ranges.append((start, float("inf")))

    return ranges

