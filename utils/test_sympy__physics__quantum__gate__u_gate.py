
def test_sympy__physics__quantum__gate__UGate():
    from sympy.physics.quantum.gate import UGate
    from sympy.matrices.immutable import ImmutableDenseMatrix
    from sympy.core.containers import Tuple
    from sympy.core.numbers import Integer
    assert _test_args(
        UGate(Tuple(Integer(1)), ImmutableDenseMatrix([[1, 0], [0, 2]])))

