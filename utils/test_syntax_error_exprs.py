
def test_syntax_error_exprs(engine, parser):
    e = "s +"
    with pytest.raises(SyntaxError, match="invalid syntax"):
        pd.eval(e, engine=engine, parser=parser)

