
def test_polynomial_fit(calc_logdet, lamb):
    """Test that _polynomial_fit works as expected."""
    n = 20
    y = np.sin(2 * np.pi * np.linspace(0, 1, n))
    poly, logdet = _polynomial_fit(y, lamb, calc_logdet=calc_logdet)

    if not calc_logdet:
        assert logdet == 0
    
    poly2, logdet2 = _polynomial_fit(
        y, lamb, weights=1.23 * np.ones(n), calc_logdet=calc_logdet
    )
    assert logdet2 == pytest.approx(logdet, rel=1e-12)
    assert_allclose(poly2, poly)

