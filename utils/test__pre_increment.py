
def test_PreIncrement():
    p = PreIncrement(x)
    assert p.func(*p.args) == p
    assert ccode(p) == '++(x)'

