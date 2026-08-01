
def test_pinv():
    # Pseudoinverse of an invertible matrix is the inverse.
    A1 = Matrix([[a, b], [c, d]])
    assert simplify(A1.pinv(method="RD")) == simplify(A1.inv())

    # Test the four properties of the pseudoinverse for various matrices.
    As = [Matrix([[13, 104], [2212, 3], [-3, 5]]),
          Matrix([[1, 7, 9], [11, 17, 19]]),
          Matrix([a, b])]

    for A in As:
        A_pinv = A.pinv(method="RD")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

    # XXX Pinv with diagonalization makes expression too complicated.
    for A in As:
        A_pinv = simplify(A.pinv(method="ED"))
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

    # XXX Computing pinv using diagonalization makes an expression that
    # is too complicated to simplify.
    # A1 = Matrix([[a, b], [c, d]])
    # assert simplify(A1.pinv(method="ED")) == simplify(A1.inv())
    # so this is tested numerically at a fixed random point

    from sympy.core.numbers import comp
    q = A1.pinv(method="ED")
    w = A1.inv()
    reps = {a: -73633, b: 11362, c: 55486, d: 62570}
    assert all(
        comp(i.n(), j.n())
        for i, j in zip(q.subs(reps), w.subs(reps))
        )


def test_pinv():
    # Pseudoinverse of an invertible matrix is the inverse.
    A1 = Matrix([[a, b], [c, d]])
    assert simplify(A1.pinv(method="RD")) == simplify(A1.inv())

    # Test the four properties of the pseudoinverse for various matrices.
    As = [Matrix([[13, 104], [2212, 3], [-3, 5]]),
          Matrix([[1, 7, 9], [11, 17, 19]]),
          Matrix([a, b])]

    for A in As:
        A_pinv = A.pinv(method="RD")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

    # XXX Pinv with diagonalization makes expression too complicated.
    for A in As:
        A_pinv = simplify(A.pinv(method="ED"))
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

    # XXX Computing pinv using diagonalization makes an expression that
    # is too complicated to simplify.
    # A1 = Matrix([[a, b], [c, d]])
    # assert simplify(A1.pinv(method="ED")) == simplify(A1.inv())
    # so this is tested numerically at a fixed random point

    from sympy.core.numbers import comp
    q = A1.pinv(method="ED")
    w = A1.inv()
    reps = {a: -73633, b: 11362, c: 55486, d: 62570}
    assert all(
        comp(i.n(), j.n())
        for i, j in zip(q.subs(reps), w.subs(reps))
        )

