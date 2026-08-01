
def test_collect_4():
    """Collect with respect to a power"""
    a, b, c, x = symbols('a,b,c,x')

    assert collect(a*x**c + b*x**c, x**c) == x**c*(a + b)
    # issue 6096: 2 stays with c (unless c is integer or x is positive0
    assert collect(a*x**(2*c) + b*x**(2*c), x**c) == x**(2*c)*(a + b)

