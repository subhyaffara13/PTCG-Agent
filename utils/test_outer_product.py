
def test_outer_product():
    k = Ket('k')
    b = Bra('b')
    op = OuterProduct(k, b)

    assert isinstance(op, OuterProduct)
    assert isinstance(op, Operator)

    assert op.ket == k
    assert op.bra == b
    assert op.label == (k, b)
    assert op.is_commutative is False

    op = k*b

    assert isinstance(op, OuterProduct)
    assert isinstance(op, Operator)

    assert op.ket == k
    assert op.bra == b
    assert op.label == (k, b)
    assert op.is_commutative is False

    op = 2*k*b

    assert op == Mul(Integer(2), k, b)

    op = 2*(k*b)

    assert op == Mul(Integer(2), OuterProduct(k, b))

    assert Dagger(k*b) == OuterProduct(Dagger(b), Dagger(k))
    assert Dagger(k*b).is_commutative is False

    #test the _eval_trace
    assert Tr(OuterProduct(JzKet(1, 1), JzBra(1, 1))).doit() == 1

    # test scaled kets and bras
    assert OuterProduct(2 * k, b) == 2 * OuterProduct(k, b)
    assert OuterProduct(k, 2 * b) == 2 * OuterProduct(k, b)

    # test sums of kets and bras
    k1, k2 = Ket('k1'), Ket('k2')
    b1, b2 = Bra('b1'), Bra('b2')
    assert (OuterProduct(k1 + k2, b1) ==
            OuterProduct(k1, b1) + OuterProduct(k2, b1))
    assert (OuterProduct(k1, b1 + b2) ==
            OuterProduct(k1, b1) + OuterProduct(k1, b2))
    assert (OuterProduct(1 * k1 + 2 * k2, 3 * b1 + 4 * b2) ==
            3 * OuterProduct(k1, b1) +
            4 * OuterProduct(k1, b2) +
            6 * OuterProduct(k2, b1) +
            8 * OuterProduct(k2, b2))


def test_outer_product():
    assert OuterProduct(k1, b1)*OuterProduct(k2, b2) == \
        InnerProduct(b1, k2)*OuterProduct(k1, b2)

