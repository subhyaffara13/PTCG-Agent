
def test_frame_with_zero_len_series_corner_cases():
    # GH#28600
    # easy all-float case
    df = DataFrame(
        np.random.default_rng(2).standard_normal(6).reshape(3, 2), columns=["A", "B"]
    )
    ser = Series(dtype=np.float64)

    result = df + ser
    expected = DataFrame(df.values * np.nan, columns=df.columns)
    tm.assert_frame_equal(result, expected)

    with pytest.raises(ValueError, match="not aligned"):
        # Automatic alignment for comparisons deprecated GH#36795, enforced 2.0
        df == ser

    # non-float case should not raise TypeError on comparison
    df2 = DataFrame(df.values.view("M8[ns]"), columns=df.columns)
    with pytest.raises(ValueError, match="not aligned"):
        # Automatic alignment for comparisons deprecated
        df2 == ser

