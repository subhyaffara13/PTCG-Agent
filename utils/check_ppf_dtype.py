
def check_ppf_dtype(distfn, arg):
    q0 = np.asarray([0.25, 0.5, 0.75])
    q_cast = [q0.astype(tp) for tp in (np.float16, np.float32, np.float64)]
    for q in q_cast:
        for meth in [distfn.ppf, distfn.isf]:
            val = meth(q, *arg)
            npt.assert_(val.dtype == np.float64)

