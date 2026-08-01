
def fpback(R_p, y):
    """Backsubsitution solve upper triangular banded `R @ c = y.`

    `R` is in the "packed" format: `R[i, :]` is `a[i, i:i+k+1]`
    """
    R = R_p.a
    _, nz = R.shape
    nc = R_p.nc
    assert y.shape[0] == R.shape[0]

    c = np.zeros_like(y[:nc])
    c[nc-1, ...] = y[nc-1] / R[nc-1, 0]
    for i in range(nc-2, -1, -1):
        nel = min(nz, nc-i)
        # NB: broadcast R across trailing dimensions of `c`.
        summ = (R[i, 1:nel, None] * c[i+1:i+nel, ...]).sum(axis=0)
        c[i, ...] = ( y[i] - summ ) / R[i, 0]
    return c

