
def test_multiindex_columns_index_col_with_data(all_parsers):
    # GH#38292
    parser = all_parsers
    result = parser.read_csv(
        StringIO("a0,a1,a2\nb0,b1,b2\ndata,data,data"), header=[0, 1], index_col=0
    )
    expected = DataFrame(
        [["data", "data"]],
        columns=MultiIndex.from_arrays(
            [["a1", "a2"], ["b1", "b2"]], names=["a0", "b0"]
        ),
        index=Index(["data"]),
    )
    tm.assert_frame_equal(result, expected)

