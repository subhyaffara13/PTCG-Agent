
def test_weights_intact():
    # regression test for gh-9709: weights are not modified
    rng = np.random.default_rng(12345)
    vals = rng.lognormal(size=100)
    weights = rng.choice([1.0, 10.0, 100], size=vals.size)
    orig_weights = weights.copy()

    stats.gaussian_kde(np.log10(vals), weights=weights)
    assert_allclose(weights, orig_weights, atol=1e-14, rtol=1e-14)

