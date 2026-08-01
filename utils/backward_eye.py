
def backward_eye(n):
    '''
    Returns the backward identity matrix of dimensions n x n.

    Needed to "turn" the Bezout matrices
    so that the leading coefficients are first.
    See docstring of the function bezout(p, q, x, method='bz').
    '''
    M = eye(n)  # identity matrix of order n

    for i in range(int(M.rows / 2)):
        M.row_swap(0 + i, M.rows - 1 - i)

    return M

