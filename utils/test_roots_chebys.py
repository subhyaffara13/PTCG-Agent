
def test_roots_chebys():
    weightf = orth.chebys(5).weight_func
    verify_gauss_quad(sc.roots_chebys, sc.eval_chebys, weightf, -2., 2., 5)
    verify_gauss_quad(sc.roots_chebys, sc.eval_chebys, weightf, -2., 2., 25)
    verify_gauss_quad(sc.roots_chebys, sc.eval_chebys, weightf, -2., 2., 100)

    x, w = sc.roots_chebys(5, False)
    y, v, m = sc.roots_chebys(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -2, 2)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, sc.roots_chebys, 0)
    assert_raises(ValueError, sc.roots_chebys, 3.3)  # type: ignore[call-overload]

