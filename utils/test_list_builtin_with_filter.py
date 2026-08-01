
def test_list_builtin_with_filter(filter, expected):
    backends = backend_registry.list_builtin(filter)
    assert not has_duplicates(backends)
    # Compare using sets as order is not important
    assert {*backends} == {*expected}

