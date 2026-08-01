
def test_resample_how_callables(unit):
    # GH#7929
    data = np.arange(5, dtype=np.int64)
    msg = "'d' is deprecated and will be removed in a future version."
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        ind = date_range(start="2014-01-01", periods=len(data), freq="d").as_unit(unit)
    df = DataFrame({"A": data, "B": data}, index=ind)

    def fn(x, a=1):
        return str(type(x))

    class FnClass:
        def __call__(self, x):
            return str(type(x))

    df_standard = df.resample("ME").apply(fn)
    df_lambda = df.resample("ME").apply(lambda x: str(type(x)))
    df_partial = df.resample("ME").apply(partial(fn))
    df_partial2 = df.resample("ME").apply(partial(fn, a=2))
    df_class = df.resample("ME").apply(FnClass())

    tm.assert_frame_equal(df_standard, df_lambda)
    tm.assert_frame_equal(df_standard, df_partial)
    tm.assert_frame_equal(df_standard, df_partial2)
    tm.assert_frame_equal(df_standard, df_class)

