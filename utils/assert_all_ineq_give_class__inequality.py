
def assert_all_ineq_give_class_Inequality(a, b):
    """All inequality operations on `a` and `b` result in class Inequality."""
    from sympy.core.relational import _Inequality as Inequality
    assert isinstance(a > b,  Inequality)
    assert isinstance(a >= b, Inequality)
    assert isinstance(a < b,  Inequality)
    assert isinstance(a <= b, Inequality)
    assert isinstance(b > a,  Inequality)
    assert isinstance(b >= a, Inequality)
    assert isinstance(b < a,  Inequality)
    assert isinstance(b <= a, Inequality)

