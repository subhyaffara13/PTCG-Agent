
def test_roots_hermitenorm():
    rootf = sc.roots_hermitenorm
    evalf = sc.eval_hermitenorm
    weightf = orth.hermitenorm(5).weight_func

    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 5)
    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 25, atol=1e-13)
    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 100, atol=1e-12)

    x, w = sc.roots_hermitenorm(5, False)
    y, v, m = sc.roots_hermitenorm(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -np.inf, np.inf)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, sc.roots_hermitenorm, 0)
    assert_raises(ValueError, sc.roots_hermitenorm, 3.3)  # type: ignore[call-overload]

