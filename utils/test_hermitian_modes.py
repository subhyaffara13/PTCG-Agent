
def test_hermitian_modes(D, typ, which, mattype, sigma):
    rng = np.random.default_rng(1749531706842957)
    k = 2
    eval_evec(True, D, typ, k, which, None, sigma, mattype, rng=rng)

