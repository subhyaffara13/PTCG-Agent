
def test_1st_exact_integral():
    eq = cos(f(x)) - (x*sin(f(x)) - f(x)**2)*f(x).diff(x)
    sol_1 = dsolve(eq, f(x), simplify=False, hint='1st_exact_Integral')
    assert checkodesol(eq, sol_1, order=1, solve_for_func=False)

