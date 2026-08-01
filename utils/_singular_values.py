
def _singular_values(M):
    """Compute the singular values of a Matrix

    Examples
    ========

    >>> from sympy import Matrix, Symbol
    >>> x = Symbol('x', real=True)
    >>> M = Matrix([[0, 1, 0], [0, x, 0], [-1, 0, 0]])
    >>> M.singular_values()
    [sqrt(x**2 + 1), 1, 0]

    See Also
    ========

    condition_number
    """

    if M.rows >= M.cols:
        valmultpairs = M.H.multiply(M).eigenvals()
    else:
        valmultpairs = M.multiply(M.H).eigenvals()

    # Expands result from eigenvals into a simple list
    vals = []

    for k, v in valmultpairs.items():
        vals += [sqrt(k)] * v  # dangerous! same k in several spots!

    # Pad with zeros if singular values are computed in reverse way,
    # to give consistent format.
    if len(vals) < M.cols:
        vals += [M.zero] * (M.cols - len(vals))

    # sort them in descending order
    vals.sort(reverse=True, key=default_sort_key)

    return vals

