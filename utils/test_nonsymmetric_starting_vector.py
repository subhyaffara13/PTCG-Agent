
def test_nonsymmetric_starting_vector(k, D, typ):
    rng = np.random.default_rng(174953366983161)
    A = D['mat']
    n = A.shape[0]
    v0 = rng.uniform(size=n).astype(typ)
    eval_evec(False, D, typ, k, "LM", v0, sigma=None, rng=rng)

