
def test_f_signature():
    assert str(inspect.signature(f)) == "(a, b=0, *, c=0, d=0)"

