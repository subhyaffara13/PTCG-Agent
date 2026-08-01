
def test_nonlinsolve_using_substitution():
    x, y, z, n = symbols('x, y, z, n', real = True)
    system = [(x + y)*n - y**2 + 2]
    s_x = (n*y - y**2 + 2)/n
    soln = (-s_x, y)
    assert nonlinsolve(system, [x, y]) == FiniteSet(soln)

    system = [z**2*x**2 - z**2*y**2/exp(x)]
    soln_real_1 = (y, x, 0)
    soln_real_2 = (-exp(x/2)*Abs(x), x, z)
    soln_real_3 = (exp(x/2)*Abs(x), x, z)
    soln_complex_1 = (-x*exp(x/2), x, z)
    soln_complex_2 = (x*exp(x/2), x, z)
    syms = [y, x, z]
    soln = FiniteSet(soln_real_1, soln_complex_1, soln_complex_2,\
        soln_real_2, soln_real_3)
    assert nonlinsolve(system,syms) == soln

