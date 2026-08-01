
def test_sg_coeffs_deriv_gt_polyorder(xp):
    """
    If deriv > polyorder, the coefficients should be all 0.
    This is a regression test for a bug where, e.g.,
        savgol_coeffs(5, polyorder=1, deriv=2)
    raised an error.
    """
    coeffs = savgol_coeffs(5, polyorder=1, deriv=2, xp=xp)
    xp_assert_equal(coeffs, xp.zeros(5, dtype=xp.float64))
    coeffs = savgol_coeffs(7, polyorder=4, deriv=6, xp=xp)
    xp_assert_equal(coeffs, xp.zeros(7, dtype=xp.float64))

