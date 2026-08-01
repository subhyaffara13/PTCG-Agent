
def test_choose_conv_method(xp):
    for mode in ['valid', 'same', 'full']:
        for ndim in [1, 2]:
            n, k, true_method = 8, 6, 'direct'
            x = np.random.randn(*((n,) * ndim))
            h = np.random.randn(*((k,) * ndim))

            method = choose_conv_method(x, h, mode=mode)
            assert method == true_method

            method_try, times = choose_conv_method(x, h, mode=mode, measure=True)
            assert method_try in {'fft', 'direct'}
            assert isinstance(times, dict)
            assert 'fft' in times.keys() and 'direct' in times.keys()

        n = 10
        for not_fft_conv_supp in ["complex256", "complex192"]:
            if hasattr(np, not_fft_conv_supp):
                x = np.ones(n, dtype=not_fft_conv_supp)
                h = x.copy()
                assert choose_conv_method(x, h, mode=mode) == 'direct'

        x = np.array([2**51], dtype=np.int64)
        h = x.copy()
        assert choose_conv_method(x, h, mode=mode) == 'direct'

