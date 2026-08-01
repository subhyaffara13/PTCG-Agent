
def test_multivariate_bool_as_set():
    x, y = symbols('x,y')

    assert And(x >= 0, y >= 0).as_set() == Interval(0, oo) * Interval(0, oo)
    assert Or(x >= 0, y >= 0).as_set() == S.Reals * S.Reals - \
           Interval(-oo, 0, True, True) * Interval(-oo, 0, True, True)

