
def test_Limit():
    assert Limit(sin(x)/x, x, 0) != 1
    assert Limit(sin(x)/x, x, 0).doit() == 1
    assert Limit(x, x, 0, dir='+-').args == (x, x, 0, Symbol('+-'))


def test_Limit():
    assert str(Limit(sin(x)/x, x, y)) == "Limit(sin(x)/x, x, y, dir='+')"
    assert str(Limit(1/x, x, 0)) == "Limit(1/x, x, 0, dir='+')"
    assert str(
        Limit(sin(x)/x, x, y, dir="-")) == "Limit(sin(x)/x, x, y, dir='-')"

