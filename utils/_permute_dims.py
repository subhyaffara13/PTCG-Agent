
def _permute_dims(expr, permutation, **kwargs):
    return PermuteDims(expr, permutation, canonicalize=True, **kwargs)

