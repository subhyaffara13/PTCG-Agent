
def test_datetimelike_compat_deprecated():
    # GH#55638
    df = DataFrame({"a": [1]})

    msg = "the 'check_datetimelike_compat' keyword is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        tm.assert_frame_equal(df, df, check_datetimelike_compat=True)
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        tm.assert_frame_equal(df, df, check_datetimelike_compat=False)

    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        tm.assert_series_equal(df["a"], df["a"], check_datetimelike_compat=True)
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        tm.assert_series_equal(df["a"], df["a"], check_datetimelike_compat=False)

