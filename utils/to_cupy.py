
def to_cupy(array):  # pragma: no cover
    import cupy

    if has_array_interface(array):
        return cupy.asarray(array)

    return array

