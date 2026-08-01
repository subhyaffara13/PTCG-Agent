
def test_param_poly_rischDE():
    DE = DifferentialExtension(extension={'D': [Poly(1, x)]})
    a = Poly(x**2 - x, x, field=True)
    b = Poly(1, x, field=True)
    q = [Poly(x, x, field=True), Poly(x**2, x, field=True)]
    h, A = param_poly_rischDE(a, b, q, 3, DE)

    assert A.nullspace() == [Matrix([0, 1, 1, 1], DE.t)]  # c1, c2, d1, d2
    # Solution of a*Dp + b*p = c1*q1 + c2*q2 = q2 = x**2
    # is d1*h1 + d2*h2 = h1 + h2 = x.
    assert h[0] + h[1] == Poly(x, x, domain='QQ')
    # a*Dp + b*p = q1 = x has no solution.

    a = Poly(x**2 - x, x, field=True)
    b = Poly(x**2 - 5*x + 3, x, field=True)
    q = [Poly(1, x, field=True), Poly(x, x, field=True),
         Poly(x**2, x, field=True)]
    h, A = param_poly_rischDE(a, b, q, 3, DE)

    assert A.nullspace() == [Matrix([3, -5, 1, -5, 1, 1], DE.t)]
    p = -Poly(5, DE.t)*h[0] + h[1] + h[2]  # Poly(1, x)
    assert a*derivation(p, DE) + b*p == Poly(x**2 - 5*x + 3, x, domain='QQ')

