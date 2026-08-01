
def _order_ranks(ranks, j, *, xp):
    # Reorder ascending order `ranks` according to `j`
    xp = array_namespace(ranks) if xp is None else xp
    if is_numpy(xp) or is_cupy(xp):
        ordered_ranks = xp.empty(j.shape, dtype=ranks.dtype)
        xp.put_along_axis(ordered_ranks, j, ranks, axis=-1)
    else:
        # `put_along_axis` not in array API (data-apis/array-api#177)
        #  so argsort the argsort and take_along_axis...
        j_inv = xp.argsort(j, axis=-1, stable=True)
        ordered_ranks = xp.take_along_axis(ranks, j_inv, axis=-1)
    return ordered_ranks

