
def test_invalid_method():
    with pytest.raises(ValueError, match="method must be 'table' or 'single"):
        Series(range(1)).rolling(1, method="foo")

