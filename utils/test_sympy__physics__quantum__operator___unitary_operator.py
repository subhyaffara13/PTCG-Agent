
def test_sympy__physics__quantum__operator__UnitaryOperator():
    from sympy.physics.quantum.operator import UnitaryOperator
    assert _test_args(UnitaryOperator('U'))

