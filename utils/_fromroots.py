
def _fromroots(line_f, mul_f, roots):
    """
    Helper function used to implement the ``<type>fromroots`` functions.

    Parameters
    ----------
    line_f : function(float, float) -> ndarray
        The ``<type>line`` function, such as ``polyline``
    mul_f : function(array_like, array_like) -> ndarray
        The ``<type>mul`` function, such as ``polymul``
    roots
        See the ``<type>fromroots`` functions for more detail
    """
    if len(roots) == 0:
        return np.ones(1)
    else:
        [roots] = as_series([roots], trim=False)
        roots.sort()
        p = [line_f(-r, 1) for r in roots]
        n = len(p)
        while n > 1:
            m, r = divmod(n, 2)
            tmp = [mul_f(p[i], p[i + m]) for i in range(m)]
            if r:
                tmp[0] = mul_f(tmp[0], p[-1])
            p = tmp
            n = m
        return p[0]

