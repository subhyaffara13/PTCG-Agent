
def test_prde_no_cancel():
    # b large
    DE = DifferentialExtension(extension={'D': [Poly(1, x)]})
    assert prde_no_cancel_b_large(Poly(1, x), [Poly(x**2, x), Poly(1, x)], 2, DE) == \
        ([Poly(x**2 - 2*x + 2, x), Poly(1, x)], Matrix([[1, 0, -1, 0],
                                                        [0, 1, 0, -1]], x))
    assert prde_no_cancel_b_large(Poly(1, x), [Poly(x**3, x), Poly(1, x)], 3, DE) == \
        ([Poly(x**3 - 3*x**2 + 6*x - 6, x), Poly(1, x)], Matrix([[1, 0, -1, 0],
                                                                 [0, 1, 0, -1]], x))
    assert prde_no_cancel_b_large(Poly(x, x), [Poly(x**2, x), Poly(1, x)], 1, DE) == \
        ([Poly(x, x, domain='ZZ'), Poly(0, x, domain='ZZ')], Matrix([[1, -1,  0,  0],
                                                                    [1,  0, -1,  0],
                                                                    [0,  1,  0, -1]], x))
    # b small
    # XXX: Is there a better example of a monomial with D.degree() > 2?
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t**3 + 1, t)]})

    # My original q was t**4 + t + 1, but this solution implies q == t**4
    # (c1 = 4), with some of the ci for the original q equal to 0.
    G = [Poly(t**6, t), Poly(x*t**5, t), Poly(t**3, t), Poly(x*t**2, t), Poly(1 + x, t)]
    R = QQ.frac_field(x)[t]
    assert prde_no_cancel_b_small(Poly(x*t, t), G, 4, DE) == \
        ([Poly(t**4/4 - x/12*t**3 + x**2/24*t**2 + (Rational(-11, 12) - x**3/24)*t + x/24, t),
        Poly(x/3*t**3 - x**2/6*t**2 + (Rational(-1, 3) + x**3/6)*t - x/6, t), Poly(t, t),
        Poly(0, t), Poly(0, t)], Matrix([[1, 0,              -1, 0, 0,  0,  0,  0,  0,  0],
                                         [0, 1, Rational(-1, 4), 0, 0,  0,  0,  0,  0,  0],
                                         [0, 0,               0, 0, 0,  0,  0,  0,  0,  0],
                                         [0, 0,               0, 1, 0,  0,  0,  0,  0,  0],
                                         [0, 0,               0, 0, 1,  0,  0,  0,  0,  0],
                                         [1, 0,               0, 0, 0, -1,  0,  0,  0,  0],
                                         [0, 1,               0, 0, 0,  0, -1,  0,  0,  0],
                                         [0, 0,               1, 0, 0,  0,  0, -1,  0,  0],
                                         [0, 0,               0, 1, 0,  0,  0,  0, -1,  0],
                                         [0, 0,               0, 0, 1,  0,  0,  0,  0, -1]], ring=R))

    # TODO: Add test for deg(b) <= 0 with b small
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1 + t**2, t)]})
    b = Poly(-1/x**2, t, field=True)  # deg(b) == 0
    q = [Poly(x**i*t**j, t, field=True) for i in range(2) for j in range(3)]
    h, A = prde_no_cancel_b_small(b, q, 3, DE)
    V = A.nullspace()
    R = QQ.frac_field(x)[t]
    assert len(V) == 1
    assert V[0] == Matrix([Rational(-1, 2), 0, 0, 1, 0, 0]*3, ring=R)
    assert (Matrix([h])*V[0][6:, :])[0] == Poly(x**2/2, t, domain='QQ(x)')
    assert (Matrix([q])*V[0][:6, :])[0] == Poly(x - S.Half, t, domain='QQ(x)')

