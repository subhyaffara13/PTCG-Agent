
def compare_coeffs_to_alt(window_length, order, xp):
    # For the given window_length and order, compare the results
    # of savgol_coeffs and alt_sg_coeffs for pos from 0 to window_length - 1.
    # Also include pos=None.
    for pos in [None] + list(range(window_length)):
        h1 = savgol_coeffs(window_length, order, pos=pos, use='dot', xp=xp)
        h2 = alt_sg_coeffs(window_length, order, pos=pos, xp=xp)
        xp_assert_close(
            h1, h2, atol=2e-10,
            err_msg=f"window_length = {window_length}, order = {order}, pos = {pos}"
        )

