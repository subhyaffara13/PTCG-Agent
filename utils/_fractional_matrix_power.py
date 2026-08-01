
def _fractional_matrix_power(A, p):
    """
    Compute the fractional power of a matrix.

    See the fractional_matrix_power docstring in matfuncs.py for more info.

    """
    A = np.asarray(A)
    if len(A.shape) != 2 or A.shape[0] != A.shape[1]:
        raise ValueError('expected a square matrix')
    if p == int(p):
        return np.linalg.matrix_power(A, int(p))
    # Compute singular values.
    s = svdvals(A)
    # Inverse scaling and squaring cannot deal with a singular matrix,
    # because the process of repeatedly taking square roots
    # would not converge to the identity matrix.
    if s[-1]:
        # Compute the condition number relative to matrix inversion,
        # and use this to decide between floor(p) and ceil(p).
        k2 = s[0] / s[-1]
        p1 = p - np.floor(p)
        p2 = p - np.ceil(p)
        if p1 * k2 ** (1 - p1) <= -p2 * k2:
            a = int(np.floor(p))
            b = p1
        else:
            a = int(np.ceil(p))
            b = p2
        try:
            R = _remainder_matrix_power(A, b)
            Q = np.linalg.matrix_power(A, a)
            return Q.dot(R)
        except np.linalg.LinAlgError:
            pass
    # If p is negative then we are going to give up.
    # If p is non-negative then we can fall back to generic funm.
    if p < 0:
        X = np.empty_like(A)
        X.fill(np.nan)
        return X
    else:
        p1 = p - np.floor(p)
        a = int(np.floor(p))
        b = p1
        R, info = funm(A, lambda x: pow(x, b), disp=False)
        Q = np.linalg.matrix_power(A, a)
        return Q.dot(R)

