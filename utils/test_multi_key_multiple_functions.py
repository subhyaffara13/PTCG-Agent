
def test_multi_key_multiple_functions(df):
    grouped = df.groupby(["A", "B"])["C"]

    agged = grouped.agg(["mean", "std"])
    expected = DataFrame({"mean": grouped.agg("mean"), "std": grouped.agg("std")})
    tm.assert_frame_equal(agged, expected)

