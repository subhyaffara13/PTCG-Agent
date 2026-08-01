
def _cartesian_product(arrays):
    xp = array_namespace(*arrays)

    arrays_ix = xp.meshgrid(*arrays, indexing='ij')
    result = xp.reshape(xp.stack(arrays_ix, axis=-1), (-1, len(arrays)))

    return result

