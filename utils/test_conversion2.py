
def test_conversion2():
    a = 2*list2numpy([x**2, x])
    b = list2numpy([2*x**2, 2*x])
    assert (a == b).all()

    one = Rational(1)
    zero = Rational(0)
    X = list2numpy([one, zero, zero])
    Y = one*X
    X = list2numpy([Symbol("a") + Rational(1, 2)])
    Y = X + X
    assert Y == array([1 + 2*Symbol("a")])
    Y = Y + 1
    assert Y == array([2 + 2*Symbol("a")])
    Y = X - X
    assert Y == array([0])

