
def test_sympy__physics__control__lti__TransferFunction():
    from sympy.physics.control.lti import TransferFunction
    assert _test_args(TransferFunction(2, 3, x))

