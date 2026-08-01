
def test_index_values():
    idx = date_range("2019-12-31", periods=3, freq="D")
    result = idx.values
    assert result.flags.writeable is False


def test_index_values():
    idx = Index([1, 2, 3])
    result = idx.values
    assert result.flags.writeable is False

