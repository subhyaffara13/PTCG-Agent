
def _check_clip_x(x, bounds):
    if (x < bounds[0]).any() or (x > bounds[1]).any():
        warnings.warn("Values in x were outside bounds during a "
                      "minimize step, clipping to bounds",
                      RuntimeWarning, stacklevel=3)
        x = np.clip(x, bounds[0], bounds[1])
        return x

    return x

