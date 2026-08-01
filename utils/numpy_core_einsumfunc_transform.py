
def numpy_core_einsumfunc_transform() -> nodes.Module:
    return parse(
        """
    def einsum(*operands, out=None, optimize=False, **kwargs):
        return numpy.ndarray([0, 0])
    """
    )

