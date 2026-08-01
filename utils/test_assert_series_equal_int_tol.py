
def test_assert_series_equal_int_tol():
    # GH#56646
    left = Series([81, 18, 121, 38, 74, 72, 81, 81, 146, 81, 81, 170, 74, 74])
    right = Series([72, 9, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72])
    tm.assert_series_equal(left, right, rtol=1.5)

    tm.assert_frame_equal(left.to_frame(), right.to_frame(), rtol=1.5)
    tm.assert_extension_array_equal(
        left.astype("Int64").values, right.astype("Int64").values, rtol=1.5
    )

