
def det_minor(M):
    """
    Return the ``det(M)`` computed from minors without
    introducing new nesting in products.

    See Also
    ========

    det_perm
    det_quick

    """
    n = M.rows
    if n == 2:
        return M[0, 0]*M[1, 1] - M[1, 0]*M[0, 1]
    else:
        return sum((1, -1)[i % 2]*Add(*[M[0, i]*d for d in
            Add.make_args(det_minor(M.minor_submatrix(0, i)))])
            if M[0, i] else S.Zero for i in range(n))

