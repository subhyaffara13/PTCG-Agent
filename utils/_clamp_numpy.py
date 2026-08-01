
def _clamp_numpy(a, min=None, max=None):
    if min is None:
        return np.minimum(a, max)
    if max is None:
        return np.maximum(a, min)

    return np.minimum(max, np.maximum(a, min))

