
def test_issue_5132_2():
    x, y = symbols('x, y', real=True)
    eqs = [exp(x)**2 - sin(y) + z**2]
    n = Dummy('n')
    soln_real = (log(-z**2 + sin(y))/2, z)
    lam = Lambda( n, I*(2*n*pi + arg(-z**2 + sin(y)))/2 + log(Abs(z**2 - sin(y)))/2)
    img = ImageSet(lam, S.Integers)
    # not sure about the complex soln. But it looks correct.
    soln_complex = (img, z)
    soln = FiniteSet(soln_real, soln_complex)
    assert dumeq(nonlinsolve(eqs, [x, z]), soln)

    system = [r - x**2 - y**2, tan(t) - y/x]
    s_x = sqrt(r/(tan(t)**2 + 1))
    s_y = sqrt(r/(tan(t)**2 + 1))*tan(t)
    soln = FiniteSet((s_x, s_y), (-s_x, -s_y))
    assert nonlinsolve(system, [x, y]) == soln

