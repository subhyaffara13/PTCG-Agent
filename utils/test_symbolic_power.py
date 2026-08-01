
def test_symbolic_power():
    x, n = symbols("x n")
    Q = QQ[n].get_field()
    _, Dx = DifferentialOperators(Q.old_poly_ring(x), 'Dx')
    h1 = HolonomicFunction((-1) + (x)*Dx, x) ** -n
    h2 = HolonomicFunction((n) + (x)*Dx, x)

    assert h1 == h2

