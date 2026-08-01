
def test_sympy__physics__control__lti__MIMOParallel():
    from sympy.physics.control import MIMOParallel, TransferFunction, TransferFunctionMatrix
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    tfm_1 = TransferFunctionMatrix([[tf1, tf2], [tf2, tf1]])
    tfm_2 = TransferFunctionMatrix([[tf2, tf1], [tf1, tf2]])
    assert _test_args(MIMOParallel(tfm_1, tfm_2))

