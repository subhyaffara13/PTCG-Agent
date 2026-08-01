
def f_modified_gaussian(x_arr, n, xp):
    r"""
    .. math::

        f(x, y, z, w) = x^n \sqrt{y} \exp(-y-z^2-w^2)
    """
    x, y, z, w = x_arr[:, 0], x_arr[:, 1], x_arr[:, 2], x_arr[:, 3]
    res = (x ** n[:, None]) * xp.sqrt(y) * xp.exp(-y-z**2-w**2)

    return res.T

