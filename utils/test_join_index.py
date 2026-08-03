import re

def test_join_index(float_frame):
    # left / right

    f = float_frame.loc[float_frame.index[:10], ["A", "B"]]
    f2 = float_frame.loc[float_frame.index[5:], ["C", "D"]].iloc[::-1]

    joined = f.join(f2)
    tm.assert_index_equal(f.index, joined.index)
    expected_columns = Index(["A", "B", "C", "D"])
    tm.assert_index_equal(joined.columns, expected_columns)

    joined = f.join(f2, how="left")
    tm.assert_index_equal(joined.index, f.index)
    tm.assert_index_equal(joined.columns, expected_columns)

    joined = f.join(f2, how="right")
    tm.assert_index_equal(joined.index, f2.index)
    tm.assert_index_equal(joined.columns, expected_columns)

    # inner

    joined = f.join(f2, how="inner")
    tm.assert_index_equal(joined.index, f.index[5:10])
    tm.assert_index_equal(joined.columns, expected_columns)

    # outer

    joined = f.join(f2, how="outer")
    tm.assert_index_equal(joined.index, float_frame.index.sort_values())
    tm.assert_index_equal(joined.columns, expected_columns)

    # left anti
    joined = f.join(f2, how="left_anti")
    tm.assert_index_equal(joined.index, float_frame.index[:5])
    tm.assert_index_equal(joined.columns, expected_columns)

    # right anti
    joined = f.join(f2, how="right_anti")
    tm.assert_index_equal(joined.index, float_frame.index[10:][::-1])
    tm.assert_index_equal(joined.columns, expected_columns)

    join_msg = (
        "'foo' is not a valid Merge type: left, right, inner, outer, "
        "left_anti, right_anti, cross, asof"
    )
    with pytest.raises(ValueError, match=re.escape(join_msg)):
        f.join(f2, how="foo")

    # corner case - overlapping columns
    msg = "columns overlap but no suffix"
    for how in ("outer", "left", "inner"):
        with pytest.raises(ValueError, match=msg):
            float_frame.join(float_frame, how=how)

