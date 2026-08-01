
def normalize_collection_arguments(
    collection_args: Sequence[CollectionArgument],
) -> list[CollectionArgument]:
    """Normalize collection arguments to eliminate overlapping paths and parts.

    Detects when collection arguments overlap in either paths or parts and only
    keeps the shorter prefix, or the earliest argument if duplicate, preserving
    order. The result is prefix-free.
    """
    # A quadratic algorithm is not acceptable since large inputs are possible.
    # So this uses an O(n*log(n)) algorithm which takes advantage of the
    # property that after sorting, a collection argument will immediately
    # precede collection arguments it subsumes. An O(n) algorithm is not worth
    # it.
    collection_args_sorted = sorted(
        collection_args,
        key=lambda arg: (arg.path, arg.parts, arg.parametrization or ""),
    )
    normalized: list[CollectionArgument] = []
    last_kept = None
    for arg in collection_args_sorted:
        if last_kept is None or not is_collection_argument_subsumed_by(arg, last_kept):
            normalized.append(arg)
            last_kept = arg
    normalized.sort(key=lambda arg: arg.original_index)
    return normalized

