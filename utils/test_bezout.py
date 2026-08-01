
def test_bezout():
    x = Symbol('x')

    p = -2*x**5+7*x**3+9*x**2-3*x+1
    q = -10*x**4+21*x**2+18*x-3
    assert bezout(p, q, x, 'bz').det() == sylvester(p, q, x, 2).det()
    assert bezout(p, q, x, 'bz').det() != sylvester(p, q, x, 1).det()
    assert bezout(p, q, x, 'prs') == backward_eye(5) * bezout(p, q, x, 'bz') * backward_eye(5)

