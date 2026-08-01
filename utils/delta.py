
def delta(i, j):
    """
    Returns 1 if ``i == j``, else 0.

    This is used in the multiplication of Pauli matrices.

    Examples
    ========

    >>> from sympy.physics.paulialgebra import delta
    >>> delta(1, 1)
    1
    >>> delta(2, 3)
    0
    """
    if i == j:
        return 1
    else:
        return 0

