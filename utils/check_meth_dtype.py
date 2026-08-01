
def check_meth_dtype(distfn, arg, meths):
    q0 = [0.25, 0.5, 0.75]
    x0 = distfn.ppf(q0, *arg)
    x_cast = [x0.astype(tp) for tp in (np.long, np.float16, np.float32,
                                       np.float64)]

    for x in x_cast:
        # casting may have clipped the values, exclude those
        distfn._argcheck(*arg)
        x = x[(distfn.a < x) & (x < distfn.b)]
        for meth in meths:
            val = meth(x, *arg)
            npt.assert_(val.dtype == np.float64)

