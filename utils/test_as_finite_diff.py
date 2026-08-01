
def test_as_finite_diff():
    x = symbols('x')
    f = Function('f')
    dx = Function('dx')

    _as_finite_diff(f(x).diff(x), [x-2, x-1, x, x+1, x+2])

    # Use of undefined functions in ``points``
    df_true = -f(x+dx(x)/2-dx(x+dx(x)/2)/2) / dx(x+dx(x)/2) \
              + f(x+dx(x)/2+dx(x+dx(x)/2)/2) / dx(x+dx(x)/2)
    df_test = diff(f(x), x).as_finite_difference(points=dx(x), x0=x+dx(x)/2)
    assert (df_test - df_true).simplify() == 0

