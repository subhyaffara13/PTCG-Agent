
def test_apply_differently_indexed():
    df = DataFrame(np.random.default_rng(2).standard_normal((20, 10)))

    result = df.apply(Series.describe, axis=0)
    expected = DataFrame({i: v.describe() for i, v in df.items()}, columns=df.columns)
    tm.assert_frame_equal(result, expected)

    result = df.apply(Series.describe, axis=1)
    expected = DataFrame({i: v.describe() for i, v in df.T.items()}, columns=df.index).T
    tm.assert_frame_equal(result, expected)

