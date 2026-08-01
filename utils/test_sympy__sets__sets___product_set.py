
def test_sympy__sets__sets__ProductSet():
    from sympy.sets.sets import ProductSet, Interval
    assert _test_args(ProductSet(Interval(0, 1), Interval(0, 1)))

