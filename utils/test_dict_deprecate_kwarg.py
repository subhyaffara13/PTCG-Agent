
def test_dict_deprecate_kwarg(key):
    with tm.assert_produces_warning(FutureWarning):
        assert _f2(old=key) == _f2_mappings[key]

