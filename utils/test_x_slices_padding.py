
def test_x_slices_padding():
    """Verify padding.

    The reference arrays were taken from  the docstrings of `zero_ext`,
    `const_ext`, `odd_ext()`, and `even_ext()` from the _array_tools module.
    """
    SFT = ShortTimeFFT(np.ones(5), hop=4, fs=1)
    x = np.array([[1, 2, 3, 4, 5], [0, 1, 4, 9, 16]], dtype=float)
    d = {'zeros': [[[0, 0, 1, 2, 3], [0, 0, 0, 1, 4]],
                   [[3, 4, 5, 0, 0], [4, 9, 16, 0, 0]]],
         'edge': [[[1, 1, 1, 2, 3], [0, 0, 0, 1, 4]],
                  [[3, 4, 5, 5, 5], [4, 9, 16, 16, 16]]],
         'even': [[[3, 2, 1, 2, 3], [4, 1, 0, 1, 4]],
                  [[3, 4, 5, 4, 3], [4, 9, 16, 9, 4]]],
         'odd': [[[-1, 0, 1, 2, 3], [-4, -1, 0, 1, 4]],
                 [[3, 4, 5, 6, 7], [4, 9, 16, 23, 28]]]}
    for p_, xx in d.items():
        gen = SFT._x_slices(np.array(x), 0, 0, 2, padding=cast(PAD_TYPE, p_))
        yy = np.array([y_.copy() for y_ in gen])  # due to inplace copying
        xx = np.asarray(xx, dtype=np.float64)
        xp_assert_equal(yy, xx, err_msg=f"Failed '{p_}' padding.")

