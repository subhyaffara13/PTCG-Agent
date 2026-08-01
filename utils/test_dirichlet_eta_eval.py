
def test_dirichlet_eta_eval():
    assert dirichlet_eta(0) == S.Half
    assert dirichlet_eta(-1) == Rational(1, 4)
    assert dirichlet_eta(1) == log(2)
    assert dirichlet_eta(1, S.Half).simplify() == pi/2
    assert dirichlet_eta(1, 2) == 1 - log(2)
    assert dirichlet_eta(2) == pi**2/12
    assert dirichlet_eta(4) == pi**4*Rational(7, 720)
    assert str(dirichlet_eta(I).evalf(n=10)) == '0.5325931818 + 0.2293848577*I'
    assert str(dirichlet_eta(I, I).evalf(n=10)) == '3.462349253 + 0.220285771*I'

