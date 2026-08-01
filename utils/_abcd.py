
def _abcd(M, list=False):
    """return parts of M as matrices or lists

    Examples
    ========

    >>> from sympy import Matrix
    >>> from sympy.solvers.simplex import _abcd

    >>> m = Matrix(3, 3, range(9)); m
    Matrix([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]])
    >>> a, b, c, d = _abcd(m)
    >>> a
    Matrix([
    [0, 1],
    [3, 4]])
    >>> b
    Matrix([
    [2],
    [5]])
    >>> c
    Matrix([[6, 7]])
    >>> d
    Matrix([[8]])

    The matrices can be returned as compact lists, too:

    >>> L = a, b, c, d = _abcd(m, list=True); L
    ([[0, 1], [3, 4]], [2, 5], [[6, 7]], [8])
    """

    def aslist(i):
        l = i.tolist()
        if len(l[0]) == 1:  # col vector
            return [i[0] for i in l]
        return l

    m = M[:-1, :-1], M[:-1, -1], M[-1, :-1], M[-1:, -1:]
    if not list:
        return m
    return tuple([aslist(i) for i in m])

