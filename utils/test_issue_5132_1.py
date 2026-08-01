
def test_issue_5132_1():
    system = [sqrt(x**2 + y**2) - sqrt(10), x + y - 4]
    assert nonlinsolve(system, [x, y]) == FiniteSet((1, 3), (3, 1))

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
                                            (s_complex_y, s_complex_z_2)
                                        )
    soln = soln_real + soln_complex
    assert dumeq(nonlinsolve(eqs, [y, z]), soln)

