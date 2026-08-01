
def test_groupby_multi_corner(df):
    # test that having an all-NA column doesn't mess you up
    df = df.copy()
    df["bad"] = np.nan
    agged = df.groupby(["A", "B"]).mean()

    expected = df.groupby(["A", "B"]).mean()
    expected["bad"] = np.nan

    tm.assert_frame_equal(agged, expected)

