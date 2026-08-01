
def test_invalid_local_variable_reference(engine, parser, express):
    a, b = 1, 2  # noqa: F841

    if parser != "pandas":
        with pytest.raises(SyntaxError, match="The '@' prefix is only"):
            pd.eval(express, engine=engine, parser=parser)
    else:
        with pytest.raises(SyntaxError, match="The '@' prefix is not"):
            pd.eval(express, engine=engine, parser=parser)

