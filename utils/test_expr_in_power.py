
def test_expr_in_power():
    x, n = symbols("x n")
    Q = QQ[n].get_field()
    _, Dx = DifferentialOperators(Q.old_poly_ring(x), 'Dx')
    h1 = HolonomicFunction((-1) + (x)*Dx, x) ** (n - 3)
    h2 = HolonomicFunction((-n + 3) + (x)*Dx, x)

    assert h1 == h2

