
def _recursive_mask_or(m1, m2, newmask):
    names = m1.dtype.names
    for name in names:
        current1 = m1[name]
        if current1.dtype.names is not None:
            _recursive_mask_or(current1, m2[name], newmask[name])
        else:
            umath.logical_or(current1, m2[name], newmask[name])

