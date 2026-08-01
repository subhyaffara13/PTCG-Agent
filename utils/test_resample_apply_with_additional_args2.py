
def test_resample_apply_with_additional_args2():
    # Testing dataframe
    def f(data, add_arg):
        return np.mean(data) * add_arg

    multiplier = 10

    df = DataFrame({"A": 1, "B": 2}, index=date_range("2017", periods=10))
    result = df.groupby("A").resample("D").agg(f, multiplier).astype(float)
    expected = df.groupby("A").resample("D").mean().multiply(multiplier)
    tm.assert_frame_equal(result, expected)

