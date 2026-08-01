
def test_genextreme_entropy():
    # regression test for gh-5181
    euler_gamma = 0.5772156649015329

    h = stats.genextreme.entropy(-1.0)
    assert_allclose(h, 2*euler_gamma + 1, rtol=1e-14)

    h = stats.genextreme.entropy(0)
    assert_allclose(h, euler_gamma + 1, rtol=1e-14)

    h = stats.genextreme.entropy(1.0)
    assert_equal(h, 1)

    h = stats.genextreme.entropy(-2.0, scale=10)
    assert_allclose(h, euler_gamma*3 + np.log(10) + 1, rtol=1e-14)

    h = stats.genextreme.entropy(10)
    assert_allclose(h, -9*euler_gamma + 1, rtol=1e-14)

    h = stats.genextreme.entropy(-10)
    assert_allclose(h, 11*euler_gamma + 1, rtol=1e-14)

