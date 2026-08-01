
def test_QubitBra():
    qb = Qubit(0)
    qb_bra = QubitBra(0)
    assert qb.dual_class() == QubitBra
    assert qb_bra.dual_class() == Qubit

    qb = Qubit(1, 1, 0)
    qb_bra = QubitBra(1, 1, 0)
    assert represent(qb, nqubits=3).H == represent(qb_bra, nqubits=3)

    qb = Qubit(0, 1)
    qb_bra = QubitBra(1,0)
    assert qb._eval_innerproduct_QubitBra(qb_bra) == Integer(0)

    qb_bra = QubitBra(0, 1)
    assert qb._eval_innerproduct_QubitBra(qb_bra) == Integer(1)

