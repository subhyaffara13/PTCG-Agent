
def RGS_generalized(m):
    """
    Computes the m + 1 generalized unrestricted growth strings
    and returns them as rows in matrix.

    Examples
    ========

    >>> from sympy.combinatorics.partitions import RGS_generalized
    >>> RGS_generalized(6)
    Matrix([
    [  1,   1,   1,  1,  1, 1, 1],
    [  1,   2,   3,  4,  5, 6, 0],
    [  2,   5,  10, 17, 26, 0, 0],
    [  5,  15,  37, 77,  0, 0, 0],
    [ 15,  52, 151,  0,  0, 0, 0],
    [ 52, 203,   0,  0,  0, 0, 0],
    [203,   0,   0,  0,  0, 0, 0]])
    """
    d = zeros(m + 1)
    for i in range(m + 1):
        d[0, i] = 1

    for i in range(1, m + 1):
        for j in range(m):
            if j <= m - i:
                d[i, j] = j * d[i - 1, j] + d[i - 1, j + 1]
            else:
                d[i, j] = 0
    return d

