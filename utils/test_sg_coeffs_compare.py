
def test_sg_coeffs_compare(xp):
    # Compare savgol_coeffs() to alt_sg_coeffs().
    for window_length in range(1, 8, 2):
        for order in range(window_length):
            compare_coeffs_to_alt(window_length, order, xp=xp)

