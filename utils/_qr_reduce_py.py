
def _qr_reduce_py(a_p, y, startrow=1):
    """This is a python counterpart of the `_qr_reduce` routine,
    declared in interpolate/src/__fitpack.h
    """
    from scipy.linalg.lapack import get_lapack_funcs
    dlartg = get_lapack_funcs('lartg', dtype=np.float64, ilp64='preferred')

    # unpack the packed format
    a = a_p.a
    offset = a_p.offset
    nc = a_p.nc

    m, nz = a.shape

    assert y.shape[0] == m
    R = a.copy()
    y1 = y.copy()

    for i in range(startrow, m):
        oi = offset[i]
        for j in range(oi, nc):
            # rotate only the lower diagonal
            if j >= min(i, nc):
                break

            # In dense format: diag a1[j, j] vs a1[i, j]
            c, s, r = dlartg(R[j, 0], R[i, 0])

            # rotate l.h.s.
            R[j, 0] = r
            for l in range(1, nz):
                R[j, l], R[i, l-1] = fprota(c, s, R[j, l], R[i, l])
            R[i, -1] = 0.0

            # rotate r.h.s.
            for l in range(y1.shape[1]):
                y1[j, l], y1[i, l] = fprota(c, s, y1[j, l], y1[i, l])

    # convert to packed
    offs = list(range(R.shape[0]))
    R_p = PackedMatrix(R, np.array(offs, dtype=np.int64), nc)

    return R_p, y1

