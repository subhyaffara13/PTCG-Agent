
def test_apply_mutating():
    # GH#35462 case where applied func pins a new BlockManager to a row
    df = DataFrame({"a": range(10), "b": range(10, 20)})
    df_orig = df.copy()

    def func(row):
        mgr = row._mgr
        row.loc["a"] += 1
        assert row._mgr is not mgr
        return row

    expected = df.copy()
    expected["a"] += 1

    result = df.apply(func, axis=1)

    tm.assert_frame_equal(result, expected)
    tm.assert_frame_equal(df, df_orig)

