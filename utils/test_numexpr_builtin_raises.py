
def test_numexpr_builtin_raises(engine, parser):
    sin, dotted_line = 1, 2
    if engine == "numexpr":
        msg = "Variables in expression .+"
        with pytest.raises(NumExprClobberingError, match=msg):
            pd.eval("sin + dotted_line", engine=engine, parser=parser)
    else:
        res = pd.eval("sin + dotted_line", engine=engine, parser=parser)
        assert res == sin + dotted_line

