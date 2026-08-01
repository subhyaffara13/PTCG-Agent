
def test_merge_multiindex_single_level():
    # GH52331
    df = DataFrame({"col": ["A", "B"]})
    df2 = DataFrame(
        data={"b": [100]},
        index=MultiIndex.from_tuples([("A",), ("C",)], names=["col"]),
    )
    expected = DataFrame({"col": ["A", "B"], "b": [100, np.nan]})

    result = df.merge(df2, left_on=["col"], right_index=True, how="left")
    tm.assert_frame_equal(result, expected)

