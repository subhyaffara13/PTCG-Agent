
def test_arithmetic_multiindex_column_align_with_fillvalue():
    # GH#60903
    df1 = DataFrame(
        data=[[1.0, 2.0]],
        columns=MultiIndex.from_tuples([("A", "one"), ("A", "two")]),
    )
    df2 = DataFrame(
        data=[[3.0, 4.0]],
        columns=MultiIndex.from_tuples([("B", "one"), ("B", "two")]),
    )
    expected = DataFrame(
        data=[[1.0, 2.0, 3.0, 4.0]],
        columns=MultiIndex.from_tuples(
            [("A", "one"), ("A", "two"), ("B", "one"), ("B", "two")]
        ),
    )
    result = df1.add(df2, fill_value=0)
    tm.assert_frame_equal(result, expected)

