
def test_Order():
    assert precedence(Order(x)) == PRECEDENCE["Atom"]


def test_Order():
    assert str(O(x)) == "O(x)"
    assert str(O(x**2)) == "O(x**2)"
    assert str(O(x*y)) == "O(x*y, x, y)"
    assert str(O(x, x)) == "O(x)"
    assert str(O(x, (x, 0))) == "O(x)"
    assert str(O(x, (x, oo))) == "O(x, (x, oo))"
    assert str(O(x, x, y)) == "O(x, x, y)"
    assert str(O(x, x, y)) == "O(x, x, y)"
    assert str(O(x, (x, oo), (y, oo))) == "O(x, (x, oo), (y, oo))"

