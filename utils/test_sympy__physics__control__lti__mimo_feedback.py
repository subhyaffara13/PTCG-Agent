
def test_sympy__physics__control__lti__MIMOFeedback():
    from sympy.physics.control import TransferFunction, MIMOFeedback, TransferFunctionMatrix
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    tfm_1 = TransferFunctionMatrix([[tf2, tf1], [tf1, tf2]])
    tfm_2 = TransferFunctionMatrix([[tf1, tf2], [tf2, tf1]])
    assert _test_args(MIMOFeedback(tfm_1, tfm_2))
    assert _test_args(MIMOFeedback(tfm_1, tfm_2, 1))

