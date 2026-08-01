
def test_roots_chebyu():
    weightf = orth.chebyu(5).weight_func
    verify_gauss_quad(sc.roots_chebyu, sc.eval_chebyu, weightf, -1., 1., 5)
    verify_gauss_quad(sc.roots_chebyu, sc.eval_chebyu, weightf, -1., 1., 25)
    verify_gauss_quad(sc.roots_chebyu, sc.eval_chebyu, weightf, -1., 1., 100)

    x, w = sc.roots_chebyu(5, False)
    y, v, m = sc.roots_chebyu(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -1, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, sc.roots_chebyu, 0)
    assert_raises(ValueError, sc.roots_chebyu, 3.3)  # type: ignore[call-overload]

