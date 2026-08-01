
def _has_matrix_shape(other):
    shape = getattr(other, 'shape', None)
    if shape is None:
        return False
    return isinstance(shape, tuple) and len(shape) == 2

