
def test_issue_5132_substitution():
    x, y, z, r, t = symbols('x, y, z, r, t', real=True)
    system = [r - x**2 - y**2, tan(t) - y/x]
    s_x_1 = Complement(FiniteSet(-sqrt(r/(tan(t)**2 + 1))), FiniteSet(0))
    s_x_2 = Complement(FiniteSet(sqrt(r/(tan(t)**2 + 1))), FiniteSet(0))
    s_y = sqrt(r/(tan(t)**2 + 1))*tan(t)
    soln = FiniteSet((s_x_2, s_y)) + FiniteSet((s_x_1, -s_y))
    assert substitution(system, [x, y]) == soln

    n = Dummy('n')
    eqs = [exp(x)**2 - sin(y) + z**2, 1/exp(y) - 3]
    s_real_y = -log(3)
    s_real_z = sqrt(-exp(2*x) - sin(log(3)))
    soln_real = FiniteSet((s_real_y, s_real_z), (s_real_y, -s_real_z))
    lam = Lambda(n, 2*n*I*pi + -log(3))
    s_complex_y = ImageSet(lam, S.Integers)
    lam = Lambda(n, sqrt(-exp(2*x) + sin(2*n*I*pi + -log(3))))
    s_complex_z_1 = ImageSet(lam, S.Integers)
    lam = Lambda(n, -sqrt(-exp(2*x) + sin(2*n*I*pi + -log(3))))
    s_complex_z_2 = ImageSet(lam, S.Integers)
    soln_complex = FiniteSet(
        (s_complex_y, s_complex_z_1),
        (s_complex_y, s_complex_z_2))
    soln = soln_real + soln_complex
    assert dumeq(substitution(eqs, [y, z]), soln)

