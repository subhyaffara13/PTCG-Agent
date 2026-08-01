
def test_complex_nonsymmetric_modes(D, typ, which, mattype, sigma):
    rng = np.random.default_rng(1749533536274527)
    k = 2
    eval_evec(False, D, typ, k, which, None, sigma, mattype, rng=rng)

