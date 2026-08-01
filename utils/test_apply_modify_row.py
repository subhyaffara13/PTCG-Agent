
def test_apply_modify_row():
    # Case: applying a function on each row as a Series object, where the
    # function mutates the row object (which needs to trigger CoW if row is a view)
    df = DataFrame({"A": [1, 2], "B": [3, 4]})
    df_orig = df.copy()

    def transform(row):
        row["B"] = 100
        return row

    df.apply(transform, axis=1)

    tm.assert_frame_equal(df, df_orig)

    # row Series is a copy
    df = DataFrame({"A": [1, 2], "B": ["b", "c"]})
    df_orig = df.copy()

    with tm.assert_produces_warning(None):
        df.apply(transform, axis=1)

    tm.assert_frame_equal(df, df_orig)

