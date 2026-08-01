
def test_empty_string_raises(engine, parser):
    # GH 13139
    with pytest.raises(ValueError, match="expr cannot be an empty string"):
        pd.eval("", engine=engine, parser=parser)

