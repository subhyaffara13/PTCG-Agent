
def merge_offset_ranges(
    paths: list[str],
    starts: list[int] | int,
    ends: list[int] | int,
    max_gap: int = 0,
    max_block: int | None = None,
    sort: bool = True,
) -> tuple[list[str], list[int], list[int]]:
    """Merge adjacent byte-offset ranges when the inter-range
    gap is <= `max_gap`, and when the merged byte range does not
    exceed `max_block` (if specified). By default, this function
    will re-order the input paths and byte ranges to ensure sorted
    order. If the user can guarantee that the inputs are already
    sorted, passing `sort=False` will skip the re-ordering.
    """
    # Check input
    if not isinstance(paths, list):
        raise TypeError
    if not isinstance(starts, list):
        starts = [starts] * len(paths)
    if not isinstance(ends, list):
        ends = [ends] * len(paths)
    if len(starts) != len(paths) or len(ends) != len(paths):
        raise ValueError

    # Early Return
    if len(starts) <= 1:
        return paths, starts, ends

    starts = [s or 0 for s in starts]
    # Sort by paths and then ranges if `sort=True`
    if sort:
        paths, starts, ends = (
            list(v)
            for v in zip(
                *sorted(
                    zip(paths, starts, ends),
                )
            )
        )
    remove = []
    for i, (path, start, end) in enumerate(zip(paths, starts, ends)):
        if any(
            e is not None and p == path and start >= s and end <= e and i != i2
            for i2, (p, s, e) in enumerate(zip(paths, starts, ends))
        ):
            remove.append(i)
    paths = [p for i, p in enumerate(paths) if i not in remove]
    starts = [s for i, s in enumerate(starts) if i not in remove]
    ends = [e for i, e in enumerate(ends) if i not in remove]

    if paths:
        # Loop through the coupled `paths`, `starts`, and
        # `ends`, and merge adjacent blocks when appropriate
        new_paths = paths[:1]
        new_starts = starts[:1]
        new_ends = ends[:1]
        for i in range(1, len(paths)):
            if paths[i] == paths[i - 1] and new_ends[-1] is None:
                continue
            elif (
                paths[i] != paths[i - 1]
                or ((starts[i] - new_ends[-1]) > max_gap)
                or (max_block is not None and (ends[i] - new_starts[-1]) > max_block)
            ):
                # Cannot merge with previous block.
                # Add new `paths`, `starts`, and `ends` elements
                new_paths.append(paths[i])
                new_starts.append(starts[i])
                new_ends.append(ends[i])
            else:
                # Merge with the previous block by updating the
                # last element of `ends`
                new_ends[-1] = ends[i]
        return new_paths, new_starts, new_ends

    # `paths` is empty. Just return input lists
    return paths, starts, ends

