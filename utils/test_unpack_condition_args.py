
def test_unpack_condition_args():
    """
    Verify parsing of condition arguments for `scipy.signal.find_peaks` function.
    """
    x = np.arange(10)
    amin_true = x
    amax_true = amin_true + 10
    peaks = amin_true[1::2]

    # Test unpacking with None or interval
    assert (None, None) == _unpack_condition_args((None, None), x, peaks)
    assert (1, None) == _unpack_condition_args(1, x, peaks)
    assert (1, None) == _unpack_condition_args((1, None), x, peaks)
    assert (None, 2) == _unpack_condition_args((None, 2), x, peaks)
    assert (3., 4.5) == _unpack_condition_args((3., 4.5), x, peaks)

    # Test if borders are correctly reduced with `peaks`
    amin_calc, amax_calc = _unpack_condition_args((amin_true, amax_true), x, peaks)
    xp_assert_equal(amin_calc, amin_true[peaks])
    xp_assert_equal(amax_calc, amax_true[peaks])

    # Test raises if array borders don't match x
    with raises(ValueError, match="array size of lower"):
        _unpack_condition_args(amin_true, np.arange(11), peaks)
    with raises(ValueError, match="array size of upper"):
        _unpack_condition_args((None, amin_true), np.arange(11), peaks)

