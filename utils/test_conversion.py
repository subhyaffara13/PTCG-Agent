
def test_conversion():
    f = [x**2 + y**2, 2*z]
    g = [((1, 0, 0, 1), QQ(2)), ((0, 2, 0, 0), QQ(1)), ((0, 0, 2, 0), QQ(1))]
    assert sdm_to_vector(g, [x, y, z], QQ) == f
    assert sdm_from_vector(f, lex, QQ) == g
    assert sdm_from_vector(
        [x, 1], lex, QQ) == [((1, 0), QQ(1)), ((0, 1), QQ(1))]
    assert sdm_to_vector([((1, 1, 0, 0), 1)], [x, y, z], QQ, n=3) == [0, x, 0]
    assert sdm_from_vector([0, 0], lex, QQ, gens=[x, y]) == sdm_zero()


def test_conversion():
    L = QQ.old_poly_ring(x, y, order="ilex")
    G = QQ.old_poly_ring(x, y)

    assert L.convert(x) == L.convert(G.convert(x), G)
    assert G.convert(x) == G.convert(L.convert(x), L)
    raises(CoercionFailed, lambda: G.convert(L.convert(1/(1 + x)), L))


def test_conversion():
    # StateSpace to TransferFunction for SISO
    A1 = Matrix([[-5, -1], [3, -1]])
    B1 = Matrix([2, 5])
    C1 = Matrix([[1, 2]])
    D1 = Matrix([0])
    H1 = StateSpace(A1, B1, C1, D1)
    H3 = StateSpace(Matrix([[a0, a1], [a2, a3]]), B = Matrix([[b1], [b2]]), C = Matrix([[c1, c2]]))
    tm1 = H1.rewrite(TransferFunction)
    tm2 = (-H1).rewrite(TransferFunction)

    tf1 = tm1[0][0]
    tf2 = tm2[0][0]

    assert tf1 == TransferFunction(12*s + 59, s**2 + 6*s + 8, s)
    assert tf2.num == -tf1.num
    assert tf2.den == tf1.den

    # StateSpace to TransferFunction for MIMO
    A2 = Matrix([[-1.5, -2, 3], [1, 0, 1], [2, 1, 1]])
    B2 = Matrix([[0.5, 0, 1], [0, 1, 2], [2, 2, 3]])
    C2 = Matrix([[0, 1, 0], [0, 2, 1], [1, 0, 2]])
    D2 = Matrix([[2, 2, 0], [1, 1, 1], [3, 2, 1]])
    H2 = StateSpace(A2, B2, C2, D2)
    tm3 = H2.rewrite(TransferFunction)

    # outputs for input i obtained at Index i-1. Consider input 1
    assert tm3[0][0] == TransferFunction(2.0*s**3 + 1.0*s**2 - 10.5*s + 4.5, 1.0*s**3 + 0.5*s**2 - 6.5*s - 2.5, s)
    assert tm3[0][1] == TransferFunction(2.0*s**3 + 2.0*s**2 - 10.5*s - 3.5, 1.0*s**3 + 0.5*s**2 - 6.5*s - 2.5, s)
    assert tm3[0][2] == TransferFunction(2.0*s**2 + 5.0*s - 0.5, 1.0*s**3 + 0.5*s**2 - 6.5*s - 2.5, s)
    assert H3.rewrite(TransferFunction) == [[TransferFunction(-c1*(a1*b2 - a3*b1 + b1*s) - c2*(-a0*b2 + a2*b1 + b2*s),
                                                              -a0*a3 + a0*s + a1*a2 + a3*s - s**2, s)]]
    # TransferFunction to StateSpace
    SS = TF1.rewrite(StateSpace)
    assert SS == \
        StateSpace(Matrix([[     0,          1],
                           [-wn**2, -2*wn*zeta]]),
                   Matrix([[0],
                           [1]]),
                   Matrix([[1, 0]]),
                   Matrix([[0]]))
    assert SS.rewrite(TransferFunction)[0][0] == TF1

    # Transfer function has to be proper
    raises(ValueError, lambda: TransferFunction(b*s**2 + p**2 - a*p + s, b - p**2, s).rewrite(StateSpace))


def test_conversion(Poly1, Poly2):
    x = np.linspace(0, 1, 10)
    coef = random((3,))

    d1 = Poly1.domain + random((2,)) * .25
    w1 = Poly1.window + random((2,)) * .25
    p1 = Poly1(coef, domain=d1, window=w1)

    d2 = Poly2.domain + random((2,)) * .25
    w2 = Poly2.window + random((2,)) * .25
    p2 = p1.convert(kind=Poly2, domain=d2, window=w2)

    assert_almost_equal(p2.domain, d2)
    assert_almost_equal(p2.window, w2)
    assert_almost_equal(p2(x), p1(x))

