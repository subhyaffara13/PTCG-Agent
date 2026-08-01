
def test_real_nonsymmetric_modes(D, typ, which, mattype,
                                 sigma, OPpart):
    rng = np.random.default_rng(174953334412726)
    k = 2
    eval_evec(False, D, typ, k, which, None, sigma, mattype, OPpart, rng=rng)

