
def test_choose_conv_method_2(xp):
    for mode in ['valid', 'same', 'full']:
        n = 10
        for not_fft_conv_supp in ["complex256", "complex192"]:
            if hasattr(np, not_fft_conv_supp):
                x = np.ones(n, dtype=not_fft_conv_supp)
                h = x.copy()
                assert choose_conv_method(x, h, mode=mode) == 'direct'

