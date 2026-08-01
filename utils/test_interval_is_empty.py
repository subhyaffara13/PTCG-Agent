
def test_interval_is_empty():
    x, y = symbols('x, y')
    r = Symbol('r', real=True)
    p = Symbol('p', positive=True)
    n = Symbol('n', negative=True)
    nn = Symbol('nn', nonnegative=True)
    assert Interval(1, 2).is_empty == False
    assert Interval(3, 3).is_empty == False  # FiniteSet
    assert Interval(r, r).is_empty == False  # FiniteSet
    assert Interval(r, r + nn).is_empty == False
    assert Interval(x, x).is_empty == False
    assert Interval(1, oo).is_empty == False
    assert Interval(-oo, oo).is_empty == False
    assert Interval(-oo, 1).is_empty == False
    assert Interval(x, y).is_empty == None
    assert Interval(r, oo).is_empty == False  # real implies finite
    assert Interval(n, 0).is_empty == False
    assert Interval(n, 0, left_open=True).is_empty == False
    assert Interval(p, 0).is_empty == True  # EmptySet
    assert Interval(nn, 0).is_empty == None
    assert Interval(n, p).is_empty == False
    assert Interval(0, p, left_open=True).is_empty == False
    assert Interval(0, p, right_open=True).is_empty == False
    assert Interval(0, nn, left_open=True).is_empty == None
    assert Interval(0, nn, right_open=True).is_empty == None

