
def test_TransferFunction_str():
    tf1 = TransferFunction(x - 1, x + 1, x)
    assert str(tf1) == "TransferFunction(x - 1, x + 1, x)"
    tf2 = TransferFunction(x + 1, 2 - y, x)
    assert str(tf2) == "TransferFunction(x + 1, 2 - y, x)"
    tf3 = TransferFunction(y, y**2 + 2*y + 3, y)
    assert str(tf3) == "TransferFunction(y, y**2 + 2*y + 3, y)"

