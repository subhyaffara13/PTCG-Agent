
def test_sg_coeffs_large(xp):
    # Test that for large values of window_length and polyorder the array of
    # coefficients returned is symmetric. The aim is to ensure that
    # no potential numeric overflow occurs.
    coeffs0 = savgol_coeffs(31, 9, xp=xp)
    xp_assert_close(
        coeffs0, xp.flip(coeffs0), atol=5e-4 if is_torch(xp) else 1.5e-6
    )

    coeffs1 = savgol_coeffs(31, 9, deriv=1, xp=xp)
    xp_assert_close(
        coeffs1, -xp.flip(coeffs1), atol=1.2e-2 if is_torch(xp) else 1.5e-6
    )

