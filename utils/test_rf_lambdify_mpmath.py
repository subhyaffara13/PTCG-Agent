
def test_rf_lambdify_mpmath():
    from sympy.utilities.lambdify import lambdify
    x, y = symbols('x,y')
    f = lambdify((x,y), rf(x, y), 'mpmath')
    maple = Float('34.007346127440197')
    us = f(4.4, 2.2)
    assert abs(us - maple)/us < 1e-15

