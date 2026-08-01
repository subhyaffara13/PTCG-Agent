
def test_sympy__physics__quantum__operator__IdentityOperator():
    with warns_deprecated_sympy():
        from sympy.physics.quantum.operator import IdentityOperator
        assert _test_args(IdentityOperator(5))

