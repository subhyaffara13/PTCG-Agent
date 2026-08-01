
def test_setulb_floatround():
    """test if setulb() violates bounds

    checks for violation due to floating point rounding error
    """

    n = 5
    m = 10
    factr = 1e7
    pgtol = 1e-5
    maxls = 20
    int_dtype = np.int64 if HAS_ILP64 else np.int32

    nbd = np.full(shape=(n,), fill_value=2, dtype=int_dtype)
    low_bnd = np.zeros(n, dtype=np.float64)
    upper_bnd = np.ones(n, dtype=np.float64)

    x0 = np.array(
        [0.8750000000000278,
         0.7500000000000153,
         0.9499999999999722,
         0.8214285714285992,
         0.6363636363636085])
    x = np.copy(x0)

    f = np.array(0.0, dtype=np.float64)
    g = np.zeros(n, dtype=np.float64)

    wa = np.zeros(2*m*n + 5*n + 11*m*m + 8*m, dtype=np.float64)
    iwa = np.zeros(3*n, dtype=int_dtype)
    task = np.zeros(2, dtype=int_dtype)
    ln_task = np.zeros(2, dtype=int_dtype)
    lsave = np.zeros(4, dtype=int_dtype)
    isave = np.zeros(44, dtype=int_dtype)
    dsave = np.zeros(29, dtype=np.float64)

    for n_iter in range(7):  # 7 steps required to reproduce error
        f, g = objfun(x)

        _lbfgsb.setulb(m, x, low_bnd, upper_bnd, nbd, f, g, factr, pgtol, wa,
                       iwa, task, lsave, isave, dsave, maxls, ln_task)

        assert (x <= upper_bnd).all() and (x >= low_bnd).all(), (
            "_lbfgsb.setulb() stepped to a point outside of the bounds")

