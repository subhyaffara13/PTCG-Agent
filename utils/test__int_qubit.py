
def test_IntQubit():
    # issue 9136
    iqb = IntQubit(0, nqubits=1)
    assert qubit_to_matrix(Qubit('0')) == qubit_to_matrix(iqb)

    qb = Qubit('1010')
    assert qubit_to_matrix(IntQubit(qb)) == qubit_to_matrix(qb)

    iqb = IntQubit(1, nqubits=1)
    assert qubit_to_matrix(Qubit('1')) == qubit_to_matrix(iqb)
    assert qubit_to_matrix(IntQubit(1)) == qubit_to_matrix(iqb)

    iqb = IntQubit(7, nqubits=4)
    assert qubit_to_matrix(Qubit('0111')) == qubit_to_matrix(iqb)
    assert qubit_to_matrix(IntQubit(7, 4)) == qubit_to_matrix(iqb)

    iqb = IntQubit(8)
    assert iqb.as_int() == 8
    assert iqb.qubit_values == (1, 0, 0, 0)

    iqb = IntQubit(7, 4)
    assert iqb.qubit_values == (0, 1, 1, 1)
    assert IntQubit(3) == IntQubit(3, 2)

    #test Dual Classes
    iqb = IntQubit(3)
    iqb_bra = IntQubitBra(3)
    assert iqb.dual_class() == IntQubitBra
    assert iqb_bra.dual_class() == IntQubit

    iqb = IntQubit(5)
    iqb_bra = IntQubitBra(5)
    assert iqb._eval_innerproduct_IntQubitBra(iqb_bra) == Integer(1)

    iqb = IntQubit(4)
    iqb_bra = IntQubitBra(5)
    assert iqb._eval_innerproduct_IntQubitBra(iqb_bra) == Integer(0)
    raises(ValueError, lambda: IntQubit(4, 1))

    raises(ValueError, lambda: IntQubit('5'))
    raises(ValueError, lambda: IntQubit(5, '5'))
    raises(ValueError, lambda: IntQubit(5, nqubits='5'))
    raises(TypeError, lambda: IntQubit(5, bad_arg=True))

