
def _rectangle_small_p(a, b, eps):
    """Return ``True`` if the given rectangle is small enough. """
    (u, v), (s, t) = a, b

    if eps is not None:
        return s - u < eps and t - v < eps
    else:
        return True

