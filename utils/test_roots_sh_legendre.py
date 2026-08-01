
def test_roots_sh_legendre():
    weightf = orth.sh_legendre(5).weight_func
    verify_gauss_quad(sc.roots_sh_legendre, sc.eval_sh_legendre, weightf, 0., 1., 5)
    verify_gauss_quad(sc.roots_sh_legendre, sc.eval_sh_legendre, weightf, 0., 1.,
                      25, atol=1e-13)
    verify_gauss_quad(sc.roots_sh_legendre, sc.eval_sh_legendre, weightf, 0., 1.,
                      100, atol=1e-12)

    x, w = sc.roots_sh_legendre(5, False)
    y, v, m = sc.roots_sh_legendre(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, 0, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, sc.roots_sh_legendre, 0)
    assert_raises(ValueError, sc.roots_sh_legendre, 3.3)  # type: ignore[call-overload]

