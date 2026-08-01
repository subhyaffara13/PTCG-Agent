
def test_param_rischDE():
    DE = DifferentialExtension(extension={'D': [Poly(1, x)]})
    p1, px = Poly(1, x, field=True), Poly(x, x, field=True)
    G = [(p1, px), (p1, p1), (px, p1)]  # [1/x, 1, x]
    h, A = param_rischDE(-p1, Poly(x**2, x, field=True), G, DE)
    assert len(h) == 3
    p = [hi[0].as_expr()/hi[1].as_expr() for hi in h]
    V = A.nullspace()
    assert len(V) == 2
    assert V[0] == Matrix([-1, 1, 0, -1, 1, 0], DE.t)
    y = -p[0] + p[1] + 0*p[2]  # x
    assert y.diff(x) - y/x**2 == 1 - 1/x  # Dy + f*y == -G0 + G1 + 0*G2

    # the below test computation takes place while computing the integral
    # of 'f = log(log(x + exp(x)))'
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)]})
    G = [(Poly(t + x, t, domain='ZZ(x)'), Poly(1, t, domain='QQ')), (Poly(0, t, domain='QQ'), Poly(1, t, domain='QQ'))]
    h, A = param_rischDE(Poly(-t - 1, t, field=True), Poly(t + x, t, field=True), G, DE)
    assert len(h) == 5
    p = [hi[0].as_expr()/hi[1].as_expr() for hi in h]
    V = A.nullspace()
    assert len(V) == 3
    assert V[0] == Matrix([0, 0, 0, 0, 1, 0, 0], DE.t)
    y = 0*p[0] + 0*p[1] + 1*p[2] + 0*p[3] + 0*p[4]
    assert y.diff(t) - y/(t + x) == 0   # Dy + f*y = 0*G0 + 0*G1

