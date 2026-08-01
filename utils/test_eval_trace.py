
def test_eval_trace():
    up = JzKet(S.Half, S.Half)
    down = JzKet(S.Half, Rational(-1, 2))
    d = Density((up, 0.5), (down, 0.5))

    t = Tr(d)
    assert t.doit() == 1.0

    #test dummy time dependent states
    class TestTimeDepKet(TimeDepKet):
        def _eval_trace(self, bra, **options):
            return 1

    x, t = symbols('x t')
    k1 = TestTimeDepKet(0, 0.5)
    k2 = TestTimeDepKet(0, 1)
    d = Density([k1, 0.5], [k2, 0.5])
    assert d.doit() == (0.5 * OuterProduct(k1, k1.dual) +
                        0.5 * OuterProduct(k2, k2.dual))

    t = Tr(d)
    assert t.doit() == 1.0


def test_eval_trace():
    q1 = Qubit('10110')
    q2 = Qubit('01010')
    d = Density([q1, 0.6], [q2, 0.4])

    t = Tr(d)
    assert t.doit() == 1.0

    # extreme bits
    t = Tr(d, 0)
    assert t.doit() == (0.4*Density([Qubit('0101'), 1]) +
                        0.6*Density([Qubit('1011'), 1]))
    t = Tr(d, 4)
    assert t.doit() == (0.4*Density([Qubit('1010'), 1]) +
                        0.6*Density([Qubit('0110'), 1]))
    # index somewhere in between
    t = Tr(d, 2)
    assert t.doit() == (0.4*Density([Qubit('0110'), 1]) +
                        0.6*Density([Qubit('1010'), 1]))
    #trace all indices
    t = Tr(d, [0, 1, 2, 3, 4])
    assert t.doit() == 1.0

    # trace some indices, initialized in
    # non-canonical order
    t = Tr(d, [2, 1, 3])
    assert t.doit() == (0.4*Density([Qubit('00'), 1]) +
                        0.6*Density([Qubit('10'), 1]))

    # mixed states
    q = (1/sqrt(2)) * (Qubit('00') + Qubit('11'))
    d = Density( [q, 1.0] )
    t = Tr(d, 0)
    assert t.doit() == (0.5*Density([Qubit('0'), 1]) +
                        0.5*Density([Qubit('1'), 1]))


def test_eval_trace():
    # This test includes tests with dependencies between TensorProducts
    #and density operators. Since, the test is more to test the behavior of
    #TensorProducts it remains here

    # Density with simple tensor products as args
    t = TensorProduct(A, B)
    d = Density([t, 1.0])
    tr = Tr(d)
    assert tr.doit() == 1.0*Tr(A*Dagger(A))*Tr(B*Dagger(B))

    ## partial trace with simple tensor products as args
    t = TensorProduct(A, B, C)
    d = Density([t, 1.0])
    tr = Tr(d, [1])
    assert tr.doit() == 1.0*A*Dagger(A)*Tr(B*Dagger(B))*C*Dagger(C)

    tr = Tr(d, [0, 2])
    assert tr.doit() == 1.0*Tr(A*Dagger(A))*B*Dagger(B)*Tr(C*Dagger(C))

    # Density with multiple Tensorproducts as states
    t2 = TensorProduct(A, B)
    t3 = TensorProduct(C, D)

    d = Density([t2, 0.5], [t3, 0.5])
    t = Tr(d)
    assert t.doit() == (0.5*Tr(A*Dagger(A))*Tr(B*Dagger(B)) +
                        0.5*Tr(C*Dagger(C))*Tr(D*Dagger(D)))

    t = Tr(d, [0])
    assert t.doit() == (0.5*Tr(A*Dagger(A))*B*Dagger(B) +
                        0.5*Tr(C*Dagger(C))*D*Dagger(D))

    #Density with mixed states
    d = Density([t2 + t3, 1.0])
    t = Tr(d)
    assert t.doit() == ( 1.0*Tr(A*Dagger(A))*Tr(B*Dagger(B)) +
                        1.0*Tr(A*Dagger(C))*Tr(B*Dagger(D)) +
                        1.0*Tr(C*Dagger(A))*Tr(D*Dagger(B)) +
                        1.0*Tr(C*Dagger(C))*Tr(D*Dagger(D)))

    t = Tr(d, [1] )
    assert t.doit() == ( 1.0*A*Dagger(A)*Tr(B*Dagger(B)) +
                        1.0*A*Dagger(C)*Tr(B*Dagger(D)) +
                        1.0*C*Dagger(A)*Tr(D*Dagger(B)) +
                        1.0*C*Dagger(C)*Tr(D*Dagger(D)))

