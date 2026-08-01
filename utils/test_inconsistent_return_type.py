
def test_inconsistent_return_type():
    # GH5592
    # inconsistent return type
    df = DataFrame(
        {
            "A": ["Tiger", "Tiger", "Tiger", "Lamb", "Lamb", "Pony", "Pony"],
            "B": Series(np.arange(7), dtype="int64"),
            "C": pd.date_range("20130101", periods=7),
        }
    )

    def f_0(grp):
        return grp.iloc[0]

    expected = df.groupby("A").first()[["B"]]
    result = df.groupby("A").apply(f_0)[["B"]]
    tm.assert_frame_equal(result, expected)

    def f_1(grp):
        if grp.name == "Tiger":
            return None
        return grp.iloc[0]

    result = df.groupby("A").apply(f_1)[["B"]]
    e = expected.copy()
    e.loc["Tiger"] = np.nan
    tm.assert_frame_equal(result, e)

    def f_2(grp):
        if grp.name == "Pony":
            return None
        return grp.iloc[0]

    result = df.groupby("A").apply(f_2)[["B"]]
    e = expected.copy()
    e.loc["Pony"] = np.nan
    tm.assert_frame_equal(result, e)

    # 5592 revisited, with datetimes
    def f_3(grp):
        if grp.name == "Pony":
            return None
        return grp.iloc[0]

    result = df.groupby("A").apply(f_3)[["C"]]
    e = df.groupby("A").first()[["C"]]
    e.loc["Pony"] = pd.NaT
    tm.assert_frame_equal(result, e)

    # scalar outputs
    def f_4(grp):
        if grp.name == "Pony":
            return None
        return grp.iloc[0].loc["C"]

    result = df.groupby("A").apply(f_4)
    e = df.groupby("A").first()["C"].copy()
    e.loc["Pony"] = np.nan
    e.name = None
    tm.assert_series_equal(result, e)

