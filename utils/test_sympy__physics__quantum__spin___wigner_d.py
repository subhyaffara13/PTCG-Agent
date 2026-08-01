
def test_sympy__physics__quantum__spin__WignerD():
    from sympy.physics.quantum.spin import WignerD
    assert _test_args(WignerD(0, 1, 2, 3, 4, 5))

