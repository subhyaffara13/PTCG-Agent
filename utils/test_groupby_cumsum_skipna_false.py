
def test_groupby_cumsum_skipna_false():
    # GH#46216 don't propagate np.nan above the diagonal
    arr = np.random.default_rng(2).standard_normal((5, 5))
    df = DataFrame(arr)
    for i in range(5):
        df.iloc[i, i] = np.nan

    df["A"] = 1
    gb = df.groupby("A")

    res = gb.cumsum(skipna=False)

    expected = df[[0, 1, 2, 3, 4]].cumsum(skipna=False)
    tm.assert_frame_equal(res, expected)

