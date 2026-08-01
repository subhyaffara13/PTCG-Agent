
def test_merge_multiindex_reset_index_mixed():
    # GH#62150
    df = DataFrame(
        {("column_1", ""): [1, 1], ("column_2", ""): [2, 2]},
        index=MultiIndex.from_arrays(
            [[1, 1], ["metadata_1", "metadata_2"]], names=["index", "metadata"]
        ),
    )

    df2 = DataFrame(
        data=[1, 1],
        index=Index([1, 1], name="index"),
        columns=MultiIndex.from_product([["new_data"], [""]]),
    )

    with tm.assert_produces_warning(pd.errors.PerformanceWarning):
        result = df.reset_index().merge(df2.reset_index(), on="index")

    expected = DataFrame(
        {
            ("index", ""): [1, 1, 1, 1],
            ("metadata", ""): ["metadata_1", "metadata_1", "metadata_2", "metadata_2"],
            ("column_1", ""): [1, 1, 1, 1],
            ("column_2", ""): [2, 2, 2, 2],
            ("new_data", ""): [1, 1, 1, 1],
        }
    )
    expected.columns = MultiIndex.from_tuples(expected.columns)

    tm.assert_frame_equal(result, expected)

    result2 = df.reset_index().merge(df2.reset_index(), on=[("index", "")])
    tm.assert_frame_equal(result2, expected)

