
def _has_struct(elem):
    """Determine if elem is an array and if first array item is a struct."""
    return (isinstance(elem, np.ndarray) and (elem.size > 0) and (elem.ndim > 0) and
            isinstance(elem[0], mat_struct))

