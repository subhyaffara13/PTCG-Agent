
def test_gaussian():
    mu, x = symbols("mu x")
    sd = symbols("sd", positive=True)
    Q = QQ[mu, sd].get_field()
    e = sqrt(2)*exp(-(-mu + x)**2/(2*sd**2))/(2*sqrt(pi)*sd)
    h1 = expr_to_holonomic(e, x, domain=Q)

    _, Dx = DifferentialOperators(Q.old_poly_ring(x), 'Dx')
    h2 = HolonomicFunction((-mu/sd**2 + x/sd**2) + (1)*Dx, x)

    assert h1 == h2

