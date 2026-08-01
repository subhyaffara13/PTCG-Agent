
def test_windowfunc_basics(window, window_name, params, xp):
    window = getattr(windows, window_name)
    if is_jax(xp) and window_name in ['taylor', 'chebwin']:
        pytest.skip(reason=f'{window_name = }: item assignment')
    if window_name in ['dpss']:
        if is_cupy(xp):
            pytest.skip(reason='dpss window is not implemented for cupy')
        if is_torch(xp) and SCIPY_DEVICE != 'cpu':
            pytest.skip(reason='needs eight_tridiagonal which is CPU only')

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "This window is not suitable", UserWarning)
        # Check symmetry for odd and even lengths
        w1 = window(8, *params, sym=True, xp=xp)
        w2 = window(7, *params, sym=False, xp=xp)
        xp_assert_close(w1[:-1], w2)

        w1 = window(9, *params, sym=True, xp=xp)
        w2 = window(8, *params, sym=False, xp=xp)
        xp_assert_close(w1[:-1], w2)

        # Check that functions run and output lengths are correct
        assert window(6, *params, sym=True, xp=xp).shape[0] == 6
        assert window(6, *params, sym=False, xp=xp).shape[0] == 6
        assert window(7, *params, sym=True, xp=xp).shape[0] == 7
        assert window(7, *params, sym=False, xp=xp).shape[0] == 7

        # Check invalid lengths
        assert_raises(ValueError, window, 5.5, *params, xp=xp)
        assert_raises(ValueError, window, -7, *params, xp=xp)

        # Check degenerate cases
        xp_assert_equal(window(0, *params, sym=True, xp=xp),
                        xp.asarray([], dtype=xp.float64))
        xp_assert_equal(window(0, *params, sym=False, xp=xp),
                        xp.asarray([], dtype=xp.float64))
        xp_assert_equal(window(1, *params, sym=True, xp=xp),
                        xp.asarray([1.], dtype=xp.float64))
        xp_assert_equal(window(1, *params, sym=False, xp=xp),
                        xp.asarray([1.], dtype=xp.float64))

        # Check dtype
        assert window(0, *params, sym=True, xp=xp).dtype == xp.float64
        assert window(0, *params, sym=False, xp=xp).dtype == xp.float64
        assert window(1, *params, sym=True, xp=xp).dtype == xp.float64
        assert window(1, *params, sym=False, xp=xp).dtype == xp.float64
        assert window(6, *params, sym=True, xp=xp).dtype == xp.float64
        assert window(6, *params, sym=False, xp=xp).dtype == xp.float64

        # Check normalization
        assert xp.all(window(10, *params, sym=True, xp=xp) < 1.01)
        assert xp.all(window(10, *params, sym=False, xp=xp) < 1.01)
        assert xp.all(window(9, *params, sym=True, xp=xp) < 1.01)
        assert xp.all(window(9, *params, sym=False, xp=xp) < 1.01)

        # Check that DFT-even spectrum is purely real for odd and even
        res = fft(window(10, *params, sym=False, xp=xp))
        res = xp.imag(res)
        xp_assert_close(res, xp.zeros_like(res), atol=1e-14)

        res = fft(window(11, *params, sym=False, xp=xp))
        res = xp.imag(res)
        xp_assert_close(res, xp.zeros_like(res), atol=1e-14)

