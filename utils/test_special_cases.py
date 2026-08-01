
def test_special_cases():
    assert_equal(sc.owens_t(5, 0), 0)
    assert_allclose(sc.owens_t(0, 5), 0.5*np.arctan(5)/np.pi,
                    rtol=5e-14)
    # Target value is 0.5*Phi(5)*(1 - Phi(5)) for Phi the CDF of the
    # standard normal distribution
    assert_allclose(sc.owens_t(5, 1), 1.4332574485503512543e-07,
                    rtol=5e-14)

