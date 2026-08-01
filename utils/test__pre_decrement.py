
def test_PreDecrement():
    p = PreDecrement(x)
    assert p.func(*p.args) == p
    assert ccode(p) == '--(x)'

