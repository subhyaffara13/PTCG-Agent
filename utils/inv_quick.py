
def inv_quick(M):
    """Return the inverse of ``M``, assuming that either
    there are lots of zeros or the size of the matrix
    is small.
    """
    if not all(i.is_Number for i in M):
        if not any(i.is_Number for i in M):
            det = lambda _: det_perm(_)
        else:
            det = lambda _: det_minor(_)
    else:
        return M.inv()
    n = M.rows
    d = det(M)
    if d == S.Zero:
        raise NonInvertibleMatrixError("Matrix det == 0; not invertible")
    ret = zeros(n)
    s1 = -1
    for i in range(n):
        s = s1 = -s1
        for j in range(n):
            di = det(M.minor_submatrix(i, j))
            ret[j, i] = s*di/d
            s = -s
    return ret

