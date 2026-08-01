
def test_sympy__physics__quantum__operator__OuterProduct():
    from sympy.physics.quantum.operator import OuterProduct
    from sympy.physics.quantum import Ket, Bra
    b = Bra('b')
    k = Ket('k')
    assert _test_args(OuterProduct(k, b))

