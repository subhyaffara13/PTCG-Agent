
def test_sympy__physics__secondquant__FockState():
    from sympy.physics.secondquant import FockState
    assert _test_args(FockState((0, 1)))

