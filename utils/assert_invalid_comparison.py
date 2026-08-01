
def assert_invalid_comparison(left, right, box):
    """
    Assert that comparison operations with mismatched types behave correctly.

    Parameters
    ----------
    left : np.ndarray, ExtensionArray, Index, or Series
    right : object
    box : {pd.DataFrame, pd.Series, pd.Index, pd.array, tm.to_array}
    """
    # Not for tznaive-tzaware comparison

    # Note: not quite the same as how we do this for tm.box_expected
    xbox = box if box not in [Index, array] else np.array

    def xbox2(x):
        # Eventually we'd like this to be tighter, but for now we'll
        #  just exclude NumpyExtensionArray[bool]
        if isinstance(x, NumpyExtensionArray):
            return x._ndarray
        if isinstance(x, BooleanArray):
            # NB: we are assuming no pd.NAs for now
            return x.astype(bool)
        return x

    result = xbox2(left == right)
    expected = xbox(np.zeros(result.shape, dtype=np.bool_))

    tm.assert_equal(result, expected)

    result = xbox2(right == left)
    tm.assert_equal(result, xbox(expected))

    result = xbox2(left != right)
    tm.assert_equal(result, ~expected)

    result = xbox2(right != left)
    tm.assert_equal(result, xbox(~expected))

    msg = "|".join(
        [
            "Invalid comparison between",
            "Cannot compare type",
            "not supported between",
            "invalid type promotion",
            (
                # GH#36706 npdev 1.20.0 2020-09-28
                r"The DTypes <class 'numpy.dtype\[datetime64\]'> and "
                r"<class 'numpy.dtype\[int64\]'> do not have a common DType. "
                "For example they cannot be stored in a single array unless the "
                "dtype is `object`."
            ),
        ]
    )
    with pytest.raises(TypeError, match=msg):
        left < right
    with pytest.raises(TypeError, match=msg):
        left <= right
    with pytest.raises(TypeError, match=msg):
        left > right
    with pytest.raises(TypeError, match=msg):
        left >= right
    with pytest.raises(TypeError, match=msg):
        right < left
    with pytest.raises(TypeError, match=msg):
        right <= left
    with pytest.raises(TypeError, match=msg):
        right > left
    with pytest.raises(TypeError, match=msg):
        right >= left

