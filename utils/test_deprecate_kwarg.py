
def test_deprecate_kwarg(key, klass):
    x = 78

    with tm.assert_produces_warning(klass):
        assert _f1(**{key: x}) == x

