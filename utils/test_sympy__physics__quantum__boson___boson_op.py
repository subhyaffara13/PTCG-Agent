
def test_sympy__physics__quantum__boson__BosonOp():
    from sympy.physics.quantum.boson import BosonOp
    assert _test_args(BosonOp('a'))
    assert _test_args(BosonOp('a', False))

