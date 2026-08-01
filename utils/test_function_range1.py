
def test_function_range1():
    assert function_range(tan(x)**2 + tan(3*x)**2 + 1, x, S.Reals) == Interval(1,oo)

