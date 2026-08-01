
def test_pretty_TransferFunction():
    tf1 = TransferFunction(s - 1, s + 1, s)
    assert upretty(tf1) == "s - 1\n─────\ns + 1"
    tf2 = TransferFunction(2*s + 1, 3 - p, s)
    assert upretty(tf2) == "2⋅s + 1\n───────\n 3 - p "
    tf3 = TransferFunction(p, p + 1, p)
    assert upretty(tf3) == "  p  \n─────\np + 1"

