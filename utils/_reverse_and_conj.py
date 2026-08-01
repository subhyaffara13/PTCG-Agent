
def _reverse_and_conj(x, xp):
    """
    Reverse array `x` in all dimensions and perform the complex conjugate
    """
    if not is_torch(xp):
        reverse = (slice(None, None, -1),) * x.ndim
        x_rev = x[reverse]
    else:
        # NB: is a copy, not a view as torch does not allow negative indices
        # in slices, x-ref https://github.com/pytorch/pytorch/issues/59786
        x_rev = xp.flip(x)

    # cf https://github.com/data-apis/array-api/issues/824
    if xp.isdtype(x.dtype, 'complex floating'):
        return xp.conj(x_rev)
    else:
        return x_rev

