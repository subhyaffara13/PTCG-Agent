
def test_mismatched_na_assert_almost_equal(left, right):
    left_arr = np.array([left], dtype=object)
    right_arr = np.array([right], dtype=object)

    msg = "Mismatched null-like values"

    if left is right:
        _assert_almost_equal_both(left, right, check_dtype=False)
        tm.assert_numpy_array_equal(left_arr, right_arr)
        tm.assert_index_equal(
            Index(left_arr, dtype=object), Index(right_arr, dtype=object)
        )
        tm.assert_series_equal(
            Series(left_arr, dtype=object), Series(right_arr, dtype=object)
        )
        tm.assert_frame_equal(
            DataFrame(left_arr, dtype=object), DataFrame(right_arr, dtype=object)
        )

    else:
        with pytest.raises(AssertionError, match=msg):
            _assert_almost_equal_both(left, right, check_dtype=False)

        # TODO: to get the same deprecation in assert_numpy_array_equal we need
        #  to change/deprecate the default for strict_nan to become True
        # TODO: to get the same deprecation in assert_index_equal we need to
        #  change/deprecate array_equivalent_object to be stricter, as
        #  assert_index_equal uses Index.equal which uses array_equivalent.
        with pytest.raises(AssertionError, match="Series are different"):
            tm.assert_series_equal(
                Series(left_arr, dtype=object), Series(right_arr, dtype=object)
            )
        with pytest.raises(AssertionError, match="DataFrame.iloc.* are different"):
            tm.assert_frame_equal(
                DataFrame(left_arr, dtype=object), DataFrame(right_arr, dtype=object)
            )

