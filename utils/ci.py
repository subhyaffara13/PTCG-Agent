
def ci(a, which=95, axis=None):
    """Return a percentile range from an array of values."""
    p = 50 - which / 2, 50 + which / 2
    return np.nanpercentile(a, p, axis)


def ci(ctx, z):
    try:
        return ctx._ci(z)
    except NotImplementedError:
        return ctx._ci_generic(z)

