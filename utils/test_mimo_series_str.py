
def test_MIMOSeries_str():
    tf1 = TransferFunction(x*y**2 - z, y**3 - t**3, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tfm_1 = TransferFunctionMatrix([[tf1, tf2], [tf2, tf1]])
    tfm_2 = TransferFunctionMatrix([[tf2, tf1], [tf1, tf2]])
    assert str(MIMOSeries(tfm_1, tfm_2)) == \
        "MIMOSeries(TransferFunctionMatrix(((TransferFunction(x*y**2 - z, -t**3 + y**3, y), TransferFunction(x - y, x + y, y)), "\
            "(TransferFunction(x - y, x + y, y), TransferFunction(x*y**2 - z, -t**3 + y**3, y)))), "\
                "TransferFunctionMatrix(((TransferFunction(x - y, x + y, y), TransferFunction(x*y**2 - z, -t**3 + y**3, y)), "\
                    "(TransferFunction(x*y**2 - z, -t**3 + y**3, y), TransferFunction(x - y, x + y, y)))))"

