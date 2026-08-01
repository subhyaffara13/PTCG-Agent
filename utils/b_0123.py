
def B_0123(x, der=0):
    """A quadratic B-spline function B(x | 0, 1, 2, 3)."""
    x = np.atleast_1d(_xp_copy_to_numpy(x))
    conds = [x < 1, (x > 1) & (x < 2), x > 2]
    if der == 0:
        funcs = [lambda x: x*x/2.,
                 lambda x: 3./4 - (x-3./2)**2,
                 lambda x: (3.-x)**2 / 2]
    elif der == 2:
        funcs = [lambda x: 1.,
                 lambda x: -2.,
                 lambda x: 1.]
    else:
        raise ValueError(f'never be here: der={der}')
    pieces = np.piecewise(x, conds, funcs)
    return pieces

