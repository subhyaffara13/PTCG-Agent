
def numpy_core_multiarray_transform() -> nodes.Module:
    return parse(
        """
    # different functions defined in multiarray.py
    def inner(a, b):
        return numpy.ndarray([0, 0])

    def vdot(a, b):
        return numpy.ndarray([0, 0])
        """
    )

