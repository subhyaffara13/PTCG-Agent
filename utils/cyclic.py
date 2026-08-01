
def cyclic(n):
    """
    Generates the cyclic group of order n, Cn.

    Examples
    ========

    >>> from sympy.combinatorics.generators import cyclic
    >>> list(cyclic(5))
    [(4), (0 1 2 3 4), (0 2 4 1 3),
     (0 3 1 4 2), (0 4 3 2 1)]

    See Also
    ========

    dihedral
    """
    gen = list(range(n))
    for i in range(n):
        yield Permutation(gen)
        gen = rotate_left(gen, 1)


def cyclic(cls, n, axis=2):
    thetas = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rv = np.vstack([thetas, np.zeros(n), np.zeros(n)]).T
    return cls.from_rotvec(np.roll(rv, axis, axis=1))

