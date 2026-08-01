
def test_Union():
    from sympy.sets.sets import Interval
    assert list(unify(Interval(0, 1) + Interval(10, 11),
                      Interval(0, 1) + Interval(12, 13),
                      variables=(Interval(12, 13),)))

