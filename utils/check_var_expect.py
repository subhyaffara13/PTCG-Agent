
def check_var_expect(distfn, arg, m, v, msg):
    dist_looser_tolerances = {"rv_histogram_instance" , "ksone"}
    kwargs = {'rtol': 5e-6} if msg in dist_looser_tolerances else {}
    if np.isfinite(v):
        m2 = distfn.expect(lambda x: x*x, arg)
        npt.assert_allclose(m2, v + m*m, **kwargs)

