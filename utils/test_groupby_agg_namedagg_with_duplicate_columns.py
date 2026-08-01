
def test_groupby_agg_namedagg_with_duplicate_columns():
    # GH#58446
    df = DataFrame(
        {
            "col1": [2, 1, 1, 0, 2, 0],
            "col2": [4, 5, 36, 7, 4, 5],
            "col3": [3.1, 8.0, 12, 10, 4, 1.1],
            "col4": [17, 3, 16, 15, 5, 6],
            "col5": [-1, 3, -1, 3, -2, -1],
        }
    )

    result = df.groupby(by=["col1", "col1", "col2"], as_index=False).agg(
        new_col=pd.NamedAgg(column="col1", aggfunc="min"),
        new_col1=pd.NamedAgg(column="col1", aggfunc="max"),
        new_col2=pd.NamedAgg(column="col2", aggfunc="count"),
    )

    expected = DataFrame(
        {
            "col1": [0, 0, 1, 1, 2],
            "col2": [5, 7, 5, 36, 4],
            "new_col": [0, 0, 1, 1, 2],
            "new_col1": [0, 0, 1, 1, 2],
            "new_col2": [1, 1, 1, 1, 2],
        }
    )

    tm.assert_frame_equal(result, expected)

