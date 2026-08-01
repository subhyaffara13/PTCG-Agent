
def test_sympy__physics__control__lti__MIMOSeries():
    from sympy.physics.control import MIMOSeries, TransferFunction, TransferFunctionMatrix
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    tfm_1 = TransferFunctionMatrix([[tf2, tf1]])
    tfm_2 = TransferFunctionMatrix([[tf1, tf2], [tf2, tf1]])
    tfm_3 = TransferFunctionMatrix([[tf1], [tf2]])
    assert _test_args(MIMOSeries(tfm_3, tfm_2, tfm_1))

