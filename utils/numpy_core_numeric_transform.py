
def numpy_core_numeric_transform() -> nodes.Module:
    return parse(
        """
    # different functions defined in numeric.py
    import numpy
    def zeros_like(a, dtype=None, order='K', subok=True, shape=None): return numpy.ndarray((0, 0))
    def ones_like(a, dtype=None, order='K', subok=True, shape=None): return numpy.ndarray((0, 0))
    def full_like(a, fill_value, dtype=None, order='K', subok=True, shape=None): return numpy.ndarray((0, 0))
        """
    )

