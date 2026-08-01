
def test_agg_apply(raw):
    # passed lambda
    df = DataFrame({"A": range(5), "B": range(0, 10, 2)})

    r = df.rolling(window=3)
    a_sum = r["A"].sum()

    result = r.agg({"A": np.sum, "B": lambda x: np.std(x, ddof=1)})
    rcustom = r["B"].apply(lambda x: np.std(x, ddof=1), raw=raw)
    expected = concat([a_sum, rcustom], axis=1)
    tm.assert_frame_equal(result, expected, check_like=True)

