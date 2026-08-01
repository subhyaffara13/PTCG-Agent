
def tests_skip_nuisance(step):
    df = DataFrame({"A": range(5), "B": range(5, 10), "C": "foo"})
    r = df.rolling(window=3, step=step)
    result = r[["A", "B"]].sum()
    expected = DataFrame(
        {"A": [np.nan, np.nan, 3, 6, 9], "B": [np.nan, np.nan, 18, 21, 24]},
        columns=list("AB"),
    )[::step]
    tm.assert_frame_equal(result, expected)

