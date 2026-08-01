
def test_PostDecrement():
    p = PostDecrement(x)
    assert p.func(*p.args) == p
    assert ccode(p) == '(x)--'

