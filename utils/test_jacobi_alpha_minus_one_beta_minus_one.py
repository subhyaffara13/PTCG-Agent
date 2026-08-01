
def test_jacobi_alpha_minus_one_beta_minus_one(n, expected):
    # gh-7001 - expected values were computed with mathematica
    x = np.linspace(-1.0, 1.0, 11)
    a, b = -1, -1  # alpha, beta
    assert_allclose(_ufuncs.eval_jacobi(n, a, b, x), expected, rtol=1e-10, atol=1e-14)
    assert_allclose(
        _ufuncs.eval_jacobi(float(n), a, b, x), expected, rtol=1e-10, atol=1e-14
    )

