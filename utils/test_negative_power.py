
def test_negative_power():
    x = symbols("x")
    _, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')
    h1 = HolonomicFunction((-1) + (x)*Dx, x) ** -2
    h2 = HolonomicFunction((2) + (x)*Dx, x)

    assert h1 == h2

