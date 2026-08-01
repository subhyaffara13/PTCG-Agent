
def test_sympy__physics__secondquant__FockStateBosonBra():
    from sympy.physics.secondquant import FockStateBosonBra
    assert _test_args(FockStateBosonBra((0, 1)))

