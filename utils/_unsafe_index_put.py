
def _unsafe_index_put(x, indices, value, accumulate=False):
    return aten.index_put(x, indices, value, accumulate)


def _unsafe_index_put(x, indices, values, accumulate=False):
    return index_put_impl_(
        clone(x), indices, values, accumulate, check=False, may_realize=False
    )

