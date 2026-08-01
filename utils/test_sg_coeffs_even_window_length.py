
def test_sg_coeffs_even_window_length(xp):
    # Simple case - deriv=0, polyorder=0, 1
    window_lengths = [4, 6, 8, 10, 12, 14, 16]
    for length in window_lengths:
        h_p_d = savgol_coeffs(length, 0, 0, xp=xp)
        xp_assert_close(h_p_d, xp.ones_like(h_p_d) / length)

    # Verify with closed forms
    # deriv=1, polyorder=1, 2
    def h_p_d_closed_form_1(k, m):
        return 6*(k - 0.5)/((2*m + 1)*m*(2*m - 1))

    # deriv=2, polyorder=2
    def h_p_d_closed_form_2(k, m):
        numer = 15*(-4*m**2 + 1 + 12*(k - 0.5)**2)
        denom = 4*(2*m + 1)*(m + 1)*m*(m - 1)*(2*m - 1)
        return numer/denom

    for length in window_lengths:
        m = length//2
        expected_output = [h_p_d_closed_form_1(k, m)
                           for k in range(-m + 1, m + 1)][::-1]
        expected_output = xp.asarray(expected_output, dtype=xp.float64)
        actual_output = savgol_coeffs(length, 1, 1, xp=xp)
        xp_assert_close(actual_output, expected_output)
        actual_output = savgol_coeffs(length, 2, 1, xp=xp)
        xp_assert_close(actual_output, expected_output)

        expected_output = [h_p_d_closed_form_2(k, m)
                           for k in range(-m + 1, m + 1)][::-1]
        expected_output = xp.asarray(expected_output, dtype=xp.float64)
        actual_output = savgol_coeffs(length, 2, 2, xp=xp)
        xp_assert_close(actual_output, expected_output)
        actual_output = savgol_coeffs(length, 3, 2, xp=xp)
        xp_assert_close(actual_output, expected_output)

