
def test_copy_deprecation(meth, kwargs):
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": 1})

    if meth in ("tz_convert", "tz_localize", "to_period"):
        tz = None if meth in ("tz_localize", "to_period") else "US/Eastern"
        df.index = pd.date_range("2020-01-01", freq="D", periods=len(df), tz=tz)
    elif meth == "to_timestamp":
        df.index = pd.period_range("2020-01-01", freq="D", periods=len(df))
    elif meth == "swaplevel":
        df = df.set_index(["b", "c"])

    if meth != "swaplevel":
        with tm.assert_produces_warning(Pandas4Warning, match="copy"):
            getattr(df, meth)(copy=False, **kwargs)

    if meth != "transpose":
        with tm.assert_produces_warning(Pandas4Warning, match="copy"):
            getattr(df.a, meth)(copy=False, **kwargs)

