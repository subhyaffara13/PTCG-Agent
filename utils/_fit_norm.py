
def _fit_norm(data, floc=None, fscale=None):
    loc = floc
    scale = fscale
    if loc is None and scale is None:
        loc = np.mean(data, axis=-1)
        scale = np.std(data, ddof=1, axis=-1)
    elif loc is None:
        loc = np.mean(data, axis=-1)
    elif scale is None:
        scale = np.sqrt(((data - loc)**2).mean(axis=-1))
    return loc, scale

