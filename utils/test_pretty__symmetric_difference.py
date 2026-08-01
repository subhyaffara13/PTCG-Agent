
def test_pretty_SymmetricDifference():
    from sympy.sets.sets import SymmetricDifference
    assert upretty(SymmetricDifference(Interval(2,3), Interval(3,5), \
           evaluate = False)) == '[2, 3] ∆ [3, 5]'
    with raises(NotImplementedError):
        pretty(SymmetricDifference(Interval(2,3), Interval(3,5), evaluate = False))

