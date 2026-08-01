
def test_coefficient_properties_dop853():
    assert_allclose(np.sum(dop853_coefficients.B), 1, rtol=1e-15)
    assert_allclose(np.sum(dop853_coefficients.A, axis=1),
                    dop853_coefficients.C,
                    rtol=1e-14)

