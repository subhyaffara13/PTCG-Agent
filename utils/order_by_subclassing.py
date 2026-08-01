
def order_by_subclassing(targets: list[FullTargetInfo]) -> Iterator[FullTargetInfo]:
    """Make sure that superclass methods are always processed before subclass methods.

    This algorithm is not very optimal, but it is simple and should work well for lists
    that are already almost correctly ordered.
    """

    # First, group the targets by their TypeInfo (since targets are sorted by line,
    # we know that each TypeInfo will appear as group key only once).
    grouped = [(k, list(g)) for k, g in groupby(targets, key=lambda x: x[3])]
    remaining_infos = {info for info, _ in grouped if info is not None}

    next_group = 0
    while grouped:
        if next_group >= len(grouped):
            # This should never happen, if there is an MRO cycle, it should be reported
            # and fixed during top-level processing.
            raise ValueError("Cannot order method targets by MRO")
        next_info, group = grouped[next_group]
        if next_info is None:
            # Trivial case, not methods but functions, process them straight away.
            yield from group
            grouped.pop(next_group)
            continue
        if any(parent in remaining_infos for parent in next_info.mro[1:]):
            # We cannot process this method group yet, try a next one.
            next_group += 1
            continue
        yield from group
        grouped.pop(next_group)
        remaining_infos.discard(next_info)
        # Each time after processing a method group we should retry from start,
        # since there may be some groups that are not blocked on parents anymore.
        next_group = 0

