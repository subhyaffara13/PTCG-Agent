
def test_missing_deprecate_kwarg(key):
    with tm.assert_produces_warning(FutureWarning):
        assert _f2(old=key) == key

