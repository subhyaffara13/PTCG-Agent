
def _count_nonzero(arr):
    # XXX: a simplified count_nonzero replacement; replace once
    # https://github.com/data-apis/array-api/pull/803/ is in

    # this assumes arr.dtype == xp.bool
    xp = array_namespace(arr)
    return xp.sum(xp.astype(arr, xp.int8))

