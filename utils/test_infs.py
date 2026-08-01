
def test_infs():
    h, a = 0, np.inf
    # T(0, a) = 1/2π * arctan(a)
    res = 1/(2*np.pi) * np.arctan(a)
    assert_allclose(sc.owens_t(h, a), res, rtol=5e-14)
    assert_allclose(sc.owens_t(h, -a), -res, rtol=5e-14)

    h = 1
    # Refer Owens T function definition in Wikipedia
    # https://en.wikipedia.org/wiki/Owen%27s_T_function
    # Value approximated through Numerical Integration
    # using scipy.integrate.quad
    # quad(lambda x: 1/(2*pi)*(exp(-0.5*(1*1)*(1+x*x))/(1+x*x)), 0, inf)
    res = 0.07932762696572854
    assert_allclose(sc.owens_t(h, np.inf), res, rtol=5e-14)
    assert_allclose(sc.owens_t(h, -np.inf), -res, rtol=5e-14)

    assert_equal(sc.owens_t(np.inf, 1), 0)
    assert_equal(sc.owens_t(-np.inf, 1), 0)

    assert_equal(sc.owens_t(np.inf, np.inf), 0)
    assert_equal(sc.owens_t(-np.inf, np.inf), 0)
    assert_equal(sc.owens_t(np.inf, -np.inf), -0.0)
    assert_equal(sc.owens_t(-np.inf, -np.inf), -0.0)

