
def test_groupby_cumprod_nan_influences_other_columns():
    # GH#48064
    df = DataFrame(
        {
            "a": 1,
            "b": [1, np.nan, 2],
            "c": [1, 2, 3.0],
        }
    )
    result = df.groupby("a").cumprod(numeric_only=True, skipna=False)
    expected = DataFrame({"b": [1, np.nan, np.nan], "c": [1, 2, 6.0]})
    tm.assert_frame_equal(result, expected)

