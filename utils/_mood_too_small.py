
def _mood_too_small(samples, kwargs, axis=-1):
    x, y = samples
    m = x.shape[axis]
    n = y.shape[axis]
    N = m + n
    return N < 3

