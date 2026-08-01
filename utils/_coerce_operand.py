
def _coerce_operand(self, other):
    """Convert other to a Matrix, or check for possible scalar."""

    INVALID = None, 'invalid_type'

    # Disallow mixing Matrix and Array
    if isinstance(other, NDimArray):
        return INVALID

    is_Matrix = getattr(other, 'is_Matrix', None)

    # Return a Matrix as-is
    if is_Matrix:
        return other, 'is_matrix'

    # Try to convert numpy array, mpmath matrix etc.
    if is_Matrix is None:
        if _has_matrix_shape(other) or _has_rows_cols(other):
            return _convert_matrix(type(self), other), 'is_matrix'

    # Could be a scalar but only if not iterable...
    if not isinstance(other, Iterable):
        return other, 'possible_scalar'

    return INVALID

