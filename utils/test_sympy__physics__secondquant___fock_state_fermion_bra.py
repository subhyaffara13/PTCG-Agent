
def test_sympy__physics__secondquant__FockStateFermionBra():
    from sympy.physics.secondquant import FockStateFermionBra
    assert _test_args(FockStateFermionBra((0, 1)))

