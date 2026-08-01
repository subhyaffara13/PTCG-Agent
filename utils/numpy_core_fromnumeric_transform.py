
def numpy_core_fromnumeric_transform() -> nodes.Module:
    return parse(
        """
    def sum(a, axis=None, dtype=None, out=None, keepdims=None, initial=None):
        return numpy.ndarray([0, 0])
    """
    )

