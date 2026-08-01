
def test_sympy__physics__control__lti__TransferFunctionMatrix():
    from sympy.physics.control import TransferFunction, TransferFunctionMatrix
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    assert _test_args(TransferFunctionMatrix([[tf1, tf2]]))

