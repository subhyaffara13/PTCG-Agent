
def test_variableoffsetwindowindexer_not_dti():
    # GH 54379
    with pytest.raises(ValueError, match="index must be a DatetimeIndex."):
        VariableOffsetWindowIndexer(index="foo", offset=BusinessDay(1))

