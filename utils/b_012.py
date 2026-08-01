
def B_012(x, xp=np):
    """ A linear B-spline function B(x | 0, 1, 2)."""
    x = np.atleast_1d(_xp_copy_to_numpy(x))
    result = np.piecewise(x, [(x < 0) | (x > 2),
                            (x >= 0) & (x < 1),
                            (x >= 1) & (x <= 2)],
                           [lambda x: 0., lambda x: x, lambda x: 2.-x])
    return xp.asarray(result)

