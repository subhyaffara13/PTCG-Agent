
def _relative_degree(z, p):
    """
    Return relative degree of transfer function from zeros and poles
    """
    degree = p.shape[0] - z.shape[0]
    if degree < 0:
        raise ValueError("Improper transfer function. "
                         "Must have at least as many poles as zeros.")
    else:
        return degree


def _relative_degree(z, p):
    """
    Return relative degree of transfer function from zeros and poles.

    This is simply len(p) - len(z), which must be nonnegative.
    A ValueError is raised if len(p) < len(z).
    """
    degree = len(p) - len(z)
    if degree < 0:
        raise ValueError("Improper transfer function. "
                         "Must have at least as many poles as zeros.")
    return degree

