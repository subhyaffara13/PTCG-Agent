
def test_MatrixSymbol_wrong_dims():
    """ Test MatrixSymbol with invalid broadcastable. """
    bcs = [(), (False,), (True,), (True, False), (False, True,), (True, True)]
    for bc in bcs:
        with raises(ValueError):
            aesara_code_(X, broadcastables={X: bc})


def test_MatrixSymbol_wrong_dims():
    """ Test MatrixSymbol with invalid broadcastable. """
    bcs = [(), (False,), (True,), (True, False), (False, True,), (True, True)]
    for bc in bcs:
        with raises(ValueError):
            theano_code_(X, broadcastables={X: bc})

