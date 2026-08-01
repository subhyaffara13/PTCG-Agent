
def test_groupby_finalize_not_implemented(obj, method):
    obj.attrs = {"a": 1}
    result = method(obj.groupby([0, 0]))
    assert result.attrs == {"a": 1}

