
def test_pipe():
    assert pipe(1, inc) == 2
    assert pipe(1, inc, inc) == 3
    assert pipe(1, double, inc, iseven) is False


def test_pipe():
    df = DataFrame({"a": [1, 2, 3], "b": 1.5})
    df_orig = df.copy()

    def testfunc(df):
        return df

    df2 = df.pipe(testfunc)

    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    # mutating df2 triggers a copy-on-write for that column
    df2.iloc[0, 0] = 0
    tm.assert_frame_equal(df, df_orig)
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))


def test_pipe():
    # Test the pipe method of DataFrameGroupBy.
    # Issue #17871

    random_state = np.random.default_rng(2)

    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": random_state.standard_normal(8),
            "C": random_state.standard_normal(8),
        }
    )

    def f(dfgb):
        return dfgb.B.max() - dfgb.C.min().min()

    def square(srs):
        return srs**2

    # Note that the transformations are
    # GroupBy -> Series
    # Series -> Series
    # This then chains the GroupBy.pipe and the
    # NDFrame.pipe methods
    result = df.groupby("A").pipe(f).pipe(square)

    index = Index(["bar", "foo"], name="A")
    expected = pd.Series([3.749306591013693, 6.717707873081384], name="B", index=index)

    tm.assert_series_equal(expected, result)


def test_pipe(test_frame, _test_series):
    # GH17905

    # series
    r = _test_series.resample("h")
    expected = r.max() - r.mean()
    result = r.pipe(lambda x: x.max() - x.mean())
    tm.assert_series_equal(result, expected)

    # dataframe
    r = test_frame.resample("h")
    expected = r.max() - r.mean()
    result = r.pipe(lambda x: x.max() - x.mean())
    tm.assert_frame_equal(result, expected)


def test_pipe(func, window_size):
    # Issue #57076
    df = DataFrame(
        {
            "B": np.random.default_rng(2).standard_normal(10),
            "C": np.random.default_rng(2).standard_normal(10),
        }
    )
    r = getattr(df, func)(window_size)

    expected = r.max() - r.mean()
    result = r.pipe(lambda x: x.max() - x.mean())
    tm.assert_frame_equal(result, expected)

    expected = r.max() - 2 * r.min()
    result = r.pipe(lambda x, k: x.max() - k * x.min(), k=2)
    tm.assert_frame_equal(result, expected)

