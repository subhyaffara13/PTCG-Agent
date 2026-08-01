
def test_overwrite_warns():
    match = r".*MyAccessor.*fake.*Series.*"
    with tm.assert_produces_warning(UserWarning, match=match):
        with ensure_removed(pd.Series, "fake"):
            setattr(pd.Series, "fake", 123)
            pd.api.extensions.register_series_accessor("fake")(MyAccessor)
            s = pd.Series([1, 2])
            assert s.fake.prop == "item"

