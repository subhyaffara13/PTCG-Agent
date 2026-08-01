
def test_NumericalInverseHermite_refcycle():
    # test if NumericalInverseHermite contains a reference cycle
    dist = stats.norm()
    urng = np.random.default_rng(0)
    with assert_deallocated(NumericalInverseHermite, dist, random_state=urng) as rng:
        u = np.linspace(0, 1, num=100)
        check_cont_samples(rng, dist, dist.stats())
        assert_allclose(dist.ppf(u), rng.ppf(u))
        del rng

