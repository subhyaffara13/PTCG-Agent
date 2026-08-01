
def test_symmetric_modes(D, typ, which, mattype, sigma, mode):
    rng = np.random.default_rng(1749531508689996)
    k = 2
    eval_evec(True, D, typ, k, which, None, sigma, mattype, None, mode, rng=rng)

