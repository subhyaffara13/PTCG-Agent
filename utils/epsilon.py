
def epsilon(i, j, k):
    """
    Return 1 if i,j,k is equal to (1,2,3), (2,3,1), or (3,1,2);
    -1 if ``i``,``j``,``k`` is equal to (1,3,2), (3,2,1), or (2,1,3);
    else return 0.

    This is used in the multiplication of Pauli matrices.

    Examples
    ========

    >>> from sympy.physics.paulialgebra import epsilon
    >>> epsilon(1, 2, 3)
    1
    >>> epsilon(1, 3, 2)
    -1
    """
    if (i, j, k) in ((1, 2, 3), (2, 3, 1), (3, 1, 2)):
        return 1
    elif (i, j, k) in ((1, 3, 2), (3, 2, 1), (2, 1, 3)):
        return -1
    else:
        return 0

