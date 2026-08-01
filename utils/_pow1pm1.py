
def _pow1pm1(x, y):
    """
    Compute (1 + x)**y - 1.

    Uses expm1 and xlog1py to avoid loss of precision when
    (1 + x)**y is close to 1.

    Note that the inverse of this function with respect to x is
    ``_pow1pm1(x, 1/y)``.  That is, if

        t = _pow1pm1(x, y)

    then

        x = _pow1pm1(t, 1/y)
    """
    return np.expm1(sc.xlog1py(y, x))

