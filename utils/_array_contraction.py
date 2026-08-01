
def _array_contraction(expr, *contraction_indices, **kwargs):
    return ArrayContraction(expr, *contraction_indices, canonicalize=True, **kwargs)

