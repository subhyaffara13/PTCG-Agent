
def test_symmetric_starting_vector(k, D, typ):
    rng = np.random.default_rng(1749532110418901)
    v0 = rng.uniform(size=len(D['v0'])).astype(typ)
    eval_evec(True, D, typ, k, 'LM', v0, rng=rng)

