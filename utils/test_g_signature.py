
def test_g_signature():
    assert str(inspect.signature(g)) == "(a, *, b=0, c=0, d=0)"

