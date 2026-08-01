
def test_solve_nonlinear_trans():
    # After the transcendental equation solver these will work
    x, y = symbols('x, y', real=True)
    soln1 = FiniteSet((2*LambertW(y/2), y))
    soln2 = FiniteSet((-x*sqrt(exp(x)), y), (x*sqrt(exp(x)), y))
    soln3 = FiniteSet((x*exp(x/2), x))
    soln4 = FiniteSet(2*LambertW(y/2), y)
    assert nonlinsolve([x**2 - y**2/exp(x)], [x, y]) == soln1
    assert nonlinsolve([x**2 - y**2/exp(x)], [y, x]) == soln2
    assert nonlinsolve([x**2 - y**2/exp(x)], [y, x]) == soln3
    assert nonlinsolve([x**2 - y**2/exp(x)], [x, y]) == soln4

