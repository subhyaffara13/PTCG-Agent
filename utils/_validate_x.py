
def _validate_x(x):
    x = np.asarray(x)
    if x.ndim == 0:
        raise ValueError('x must be at least 1-D')
    return x

