
def test_more_than_one_expression_raises(engine, parser):
    with pytest.raises(SyntaxError, match="only a single expression is allowed"):
        pd.eval("1 + 1; 2 + 2", engine=engine, parser=parser)

