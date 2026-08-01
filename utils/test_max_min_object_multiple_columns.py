
def test_max_min_object_multiple_columns(using_infer_string):
    # GH#41111 case where the aggregation is valid for some columns but not
    # others; we split object blocks column-wise, consistent with
    # DataFrame._reduce

    df = DataFrame(
        {
            "A": [1, 1, 2, 2, 3],
            "B": [1, "foo", 2, "bar", False],
            "C": ["a", "b", "c", "d", "e"],
        }
    )
    df._consolidate_inplace()  # should already be consolidate, but double-check
    assert len(df._mgr.blocks) == 3 if using_infer_string else 2

    gb = df.groupby("A")

    result = gb[["C"]].max()
    # "max" is valid for column "C" but not for "B"
    ei = pd.Index([1, 2, 3], name="A")
    expected = DataFrame({"C": ["b", "d", "e"]}, index=ei)
    tm.assert_frame_equal(result, expected)

    result = gb[["C"]].min()
    # "min" is valid for column "C" but not for "B"
    ei = pd.Index([1, 2, 3], name="A")
    expected = DataFrame({"C": ["a", "c", "e"]}, index=ei)
    tm.assert_frame_equal(result, expected)

