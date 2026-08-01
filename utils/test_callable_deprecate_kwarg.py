
def test_callable_deprecate_kwarg(x):
    with tm.assert_produces_warning(FutureWarning):
        assert _f3(old=x) == _f3_mapping(x)

