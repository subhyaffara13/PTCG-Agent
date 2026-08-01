
def test_union_with_na_when_constructing_dataframe():
    # GH43222
    series1 = Series(
        (1,),
        index=MultiIndex.from_arrays(
            [Series([None], dtype="str"), Series([None], dtype="str")]
        ),
    )
    series2 = Series((10, 20), index=MultiIndex.from_tuples(((None, None), ("a", "b"))))
    result = DataFrame([series1, series2])
    expected = DataFrame({(np.nan, np.nan): [1.0, 10.0], ("a", "b"): [np.nan, 20.0]})
    tm.assert_frame_equal(result, expected)

