
def assert_all_ineq_raise_TypeError(a, b):
    raises(TypeError, lambda: a > b)
    raises(TypeError, lambda: a >= b)
    raises(TypeError, lambda: a < b)
    raises(TypeError, lambda: a <= b)
    raises(TypeError, lambda: b > a)
    raises(TypeError, lambda: b >= a)
    raises(TypeError, lambda: b < a)
    raises(TypeError, lambda: b <= a)

