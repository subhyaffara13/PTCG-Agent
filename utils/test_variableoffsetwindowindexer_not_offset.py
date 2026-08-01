
def test_variableoffsetwindowindexer_not_offset():
    # GH 54379
    idx = date_range("2020", periods=10)
    with pytest.raises(ValueError, match="offset must be a DateOffset-like object."):
        VariableOffsetWindowIndexer(index=idx, offset="foo")

