
def identity_like_generalized(a):
    a = asarray(a)
    if a.ndim >= 3:
        r = np.empty(a.shape, dtype=a.dtype)
        r[...] = identity(a.shape[-2])
        return r
    else:
        return identity(a.shape[0])

