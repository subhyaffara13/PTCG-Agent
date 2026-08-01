
def test_roots_hermite():
    rootf = sc.roots_hermite
    evalf = sc.eval_hermite
    weightf = orth.hermite(5).weight_func

    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 5)
    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 25, atol=1e-13)
    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 100, atol=1e-12)

    # Golub-Welsch branch
    x, w = sc.roots_hermite(5, False)
    y, v, m = sc.roots_hermite(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -np.inf, np.inf)
    assert_allclose(m, muI, rtol=muI_err)

    # Asymptotic branch (switch over at n >= 150)
    x, w = sc.roots_hermite(200, False)
    y, v, m = sc.roots_hermite(200, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)
    assert_allclose(sum(v), m, 1e-14, 1e-14)

    assert_raises(ValueError, sc.roots_hermite, 0)
    assert_raises(ValueError, sc.roots_hermite, 3.3)  # type: ignore[call-overload]

