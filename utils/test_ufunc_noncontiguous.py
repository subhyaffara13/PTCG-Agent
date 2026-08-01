
def test_ufunc_noncontiguous(ufunc):
    '''
    Check that contiguous and non-contiguous calls to ufuncs
    have the same results for values in range(9)
    '''
    for typ in ufunc.types:
        # types is a list of strings like ii->i
        if any(set('O?mM') & set(typ)):
            # bool, object, datetime are too irregular for this simple test
            continue
        inp, out = typ.split('->')
        args_c = [np.empty((6, 6), t) for t in inp]
        # non contiguous (2, 3 step on the two dimensions)
        args_n = [np.empty((12, 18), t)[::2, ::3] for t in inp]
        # alignment != itemsize is possible.  So create an array with such
        # an odd step manually.
        args_o = []
        for t in inp:
            orig_dt = np.dtype(t)
            off_dt = f"S{orig_dt.alignment}"  # offset by alignment
            dtype = np.dtype([("_", off_dt), ("t", orig_dt)], align=False)
            args_o.append(np.empty((6, 6), dtype=dtype)["t"])
        for a in args_c + args_n + args_o:
            a.flat = range(1, 37)

        with warnings.catch_warnings(record=True):
            warnings.filterwarnings("always")
            res_c = ufunc(*args_c)
            res_n = ufunc(*args_n)
            res_o = ufunc(*args_o)
        if len(out) == 1:
            res_c = (res_c,)
            res_n = (res_n,)
            res_o = (res_o,)
        for c_ar, n_ar, o_ar in zip(res_c, res_n, res_o):
            dt = c_ar.dtype
            if np.issubdtype(dt, np.floating):
                # for floating point results allow a small fuss in comparisons
                # since different algorithms (libm vs. intrinsics) can be used
                # for different input strides
                res_eps = np.finfo(dt).eps
                tol = 3 * res_eps
                assert_allclose(res_c, res_n, atol=tol, rtol=tol)
                assert_allclose(res_c, res_o, atol=tol, rtol=tol)
            else:
                assert_equal(c_ar, n_ar)
                assert_equal(c_ar, o_ar)

