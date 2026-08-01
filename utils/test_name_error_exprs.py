
def test_name_error_exprs(engine, parser):
    e = "s + t"
    msg = "name 's' is not defined"
    with pytest.raises(NameError, match=msg):
        pd.eval(e, engine=engine, parser=parser)

