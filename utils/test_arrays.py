
def test_arrays():
    one = Rational(1)
    zero = Rational(0)
    X = array([one, zero, zero])
    Y = one*X
    X = array([Symbol("a") + Rational(1, 2)])
    Y = X + X
    assert Y == array([1 + 2*Symbol("a")])
    Y = Y + 1
    assert Y == array([2 + 2*Symbol("a")])
    Y = X - X
    assert Y == array([0])

