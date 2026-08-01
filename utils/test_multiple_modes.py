
def test_multiple_modes(xp, filter_func, args, kwargs):
    # Test that the filters with multiple mode capabilities for different
    # dimensions give the same result as applying a single mode.
    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])
    if is_cupy(xp) and filter_func.__name__ in ['prewitt', 'sobel']:
        pytest.xfail("https://github.com/cupy/cupy/issues/9760")

    mode1 = 'reflect'
    mode2 = ['reflect', 'reflect']

    xp_assert_equal(filter_func(arr, *args, mode=mode1, **kwargs),
                    filter_func(arr, *args, mode=mode2, **kwargs))

