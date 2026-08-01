
def _get_sample_object(
    objs: list[Series | DataFrame],
    ndims: set[int],
    keys,
    names,
    levels,
    intersect: bool,
) -> tuple[Series | DataFrame, list[Series | DataFrame]]:
    # get the sample
    # want the highest ndim that we have, and must be non-empty
    # unless all objs are empty
    if len(ndims) > 1:
        max_ndim = max(ndims)
        for obj in objs:
            if obj.ndim == max_ndim and sum(obj.shape):  # type: ignore[arg-type]
                return obj, objs
    elif keys is None and names is None and levels is None and not intersect:
        # filter out the empties if we have not multi-index possibilities
        # note to keep empty Series as it affect to result columns / name
        if ndims.pop() == 2:
            non_empties = [obj for obj in objs if sum(obj.shape)]
        else:
            non_empties = objs

        if len(non_empties):
            return non_empties[0], non_empties

    return objs[0], objs

