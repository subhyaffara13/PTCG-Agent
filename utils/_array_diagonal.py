
def _array_diagonal(expr, *diagonal_indices, **kwargs):
    return ArrayDiagonal(expr, *diagonal_indices, canonicalize=True, **kwargs)

