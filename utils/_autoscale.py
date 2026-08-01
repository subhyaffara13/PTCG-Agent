
def _autoscale(A, b, c, x0):
    """
    Scales the problem according to equilibration from [12].
    Also normalizes the right hand side vector by its maximum element.
    """
    m, n = A.shape

    C = 1
    R = 1

    if A.size > 0:

        R = np.max(np.abs(A), axis=1)
        if sps.issparse(A):
            R = R.toarray().flatten()
        R[R == 0] = 1
        R = 1/_round_to_power_of_two(R)
        A = sps.diags_array(R)@A if sps.issparse(A) else A*R.reshape(m, 1)
        b = b*R

        C = np.max(np.abs(A), axis=0)
        if sps.issparse(A):
            C = C.toarray().flatten()
        C[C == 0] = 1
        C = 1/_round_to_power_of_two(C)
        A = A@sps.diags_array(C) if sps.issparse(A) else A*C
        c = c*C

    b_scale = np.max(np.abs(b)) if b.size > 0 else 1
    if b_scale == 0:
        b_scale = 1.
    b = b/b_scale

    if x0 is not None:
        x0 = x0/b_scale*(1/C)
    return A, b, c, x0, C, b_scale

