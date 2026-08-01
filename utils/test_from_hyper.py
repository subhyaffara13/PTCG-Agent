
def test_from_hyper():
    x = symbols('x')
    R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')
    p = hyper([1, 1], [Rational(3, 2)], x**2/4)
    q = HolonomicFunction((4*x) + (5*x**2 - 8)*Dx + (x**3 - 4*x)*Dx**2, x, 1, [2*sqrt(3)*pi/9, -4*sqrt(3)*pi/27 + Rational(4, 3)])
    r = from_hyper(p)
    assert r == q
    p = from_hyper(hyper([1], [Rational(3, 2)], x**2/4))
    q = HolonomicFunction(-x + (-x**2/2 + 2)*Dx + x*Dx**2, x)
    # x0 = 1
    y0 = '[sqrt(pi)*exp(1/4)*erf(1/2), -sqrt(pi)*exp(1/4)*erf(1/2)/2 + 1]'
    assert sstr(p.y0) == y0
    assert q.annihilator == p.annihilator

