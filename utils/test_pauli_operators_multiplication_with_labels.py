
def test_pauli_operators_multiplication_with_labels():

    assert qsimplify_pauli(sx1 * sx1) == 1
    assert qsimplify_pauli(sy1 * sy1) == 1
    assert qsimplify_pauli(sz1 * sz1) == 1

    assert isinstance(sx1 * sx2, Mul)
    assert isinstance(sy1 * sy2, Mul)
    assert isinstance(sz1 * sz2, Mul)

    assert qsimplify_pauli(sx1 * sy1 * sx2 * sy2) == - sz1 * sz2
    assert qsimplify_pauli(sy1 * sz1 * sz2 * sx2) == - sx1 * sy2

