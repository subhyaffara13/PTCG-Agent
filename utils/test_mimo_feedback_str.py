
def test_MIMOFeedback_str():
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    tfm_1 = TransferFunctionMatrix([[tf2, tf1], [tf1, tf2]])
    tfm_2 = TransferFunctionMatrix([[tf1, tf2], [tf2, tf1]])
    assert (str(MIMOFeedback(tfm_1, tfm_2)) \
            == "MIMOFeedback(TransferFunctionMatrix(((TransferFunction(-x + y, y + z, x), TransferFunction(x**2 - y**3, y - z, x))," \
            " (TransferFunction(x**2 - y**3, y - z, x), TransferFunction(-x + y, y + z, x)))), " \
            "TransferFunctionMatrix(((TransferFunction(x**2 - y**3, y - z, x), " \
            "TransferFunction(-x + y, y + z, x)), (TransferFunction(-x + y, y + z, x), TransferFunction(x**2 - y**3, y - z, x)))), -1)")
    assert (str(MIMOFeedback(tfm_1, tfm_2, 1)) \
            == "MIMOFeedback(TransferFunctionMatrix(((TransferFunction(-x + y, y + z, x), TransferFunction(x**2 - y**3, y - z, x)), " \
            "(TransferFunction(x**2 - y**3, y - z, x), TransferFunction(-x + y, y + z, x)))), " \
            "TransferFunctionMatrix(((TransferFunction(x**2 - y**3, y - z, x), TransferFunction(-x + y, y + z, x)), "\
            "(TransferFunction(-x + y, y + z, x), TransferFunction(x**2 - y**3, y - z, x)))), 1)")

