import itertools

def test_nextafter_0():
    for t, direction in itertools.product(np._core.sctypes['float'], (1, -1)):
        # The value of tiny for double double is NaN, so we need to pass the
        # assert
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            if not np.isnan(np.finfo(t).tiny):
                tiny = np.finfo(t).tiny
                assert_(
                    0. < direction * np.nextafter(t(0), t(direction)) < tiny)
        assert_equal(np.nextafter(t(0), t(direction)) / t(2.1), direction * 0.0)

