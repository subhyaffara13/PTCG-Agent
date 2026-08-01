
def _unsafe_index(x, indices):
    return aten.index(x, indices)


def _unsafe_index(x, indices):
    return index_impl(x, indices, check=False)

