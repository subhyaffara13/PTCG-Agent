
def test_groupby_finalize(obj, method):
    obj.attrs = {"a": 1}
    result = method(obj.groupby([0, 0], group_keys=False))
    assert result.attrs == {"a": 1}

