
def test_sympy__physics__secondquant__FockStateKet():
    from sympy.physics.secondquant import FockStateKet
    assert _test_args(FockStateKet((0, 1)))

