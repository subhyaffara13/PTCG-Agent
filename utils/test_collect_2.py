
def test_collect_2():
    """Collect with respect to a sum"""
    a, b, x = symbols('a,b,x')
    assert collect(a*(cos(x) + sin(x)) + b*(cos(x) + sin(x)),
        sin(x) + cos(x)) == (a + b)*(cos(x) + sin(x))

