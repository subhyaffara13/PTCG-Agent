
def test_riemann_xi_eval():
    assert riemann_xi(2) == pi/6
    assert riemann_xi(0) == Rational(1, 2)
    assert riemann_xi(1) == Rational(1, 2)
    assert riemann_xi(3).rewrite(zeta) == 3*zeta(3)/(2*pi)
    assert riemann_xi(4) == pi**2/15

