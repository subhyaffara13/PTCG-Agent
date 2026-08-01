
def test_PostIncrement():
    p = PostIncrement(x)
    assert p.func(*p.args) == p
    assert ccode(p) == '(x)++'

