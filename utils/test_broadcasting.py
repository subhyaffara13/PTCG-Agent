
def test_broadcasting():
    """ Test "broadcastable" attribute after applying element-wise binary op. """

    expr = x + y

    cases = [
        [(), (), ()],
        [(False,), (False,), (False,)],
        [(True,), (False,), (False,)],
        [(False, True), (False, False), (False, False)],
        [(True, False), (False, False), (False, False)],
    ]

    for bc1, bc2, bc3 in cases:
        comp = aesara_code_(expr, broadcastables={x: bc1, y: bc2})
        assert comp.broadcastable == bc3


def test_broadcasting():
    """ Test "broadcastable" attribute after applying element-wise binary op. """

    expr = x + y

    cases = [
        [(), (), ()],
        [(False,), (False,), (False,)],
        [(True,), (False,), (False,)],
        [(False, True), (False, False), (False, False)],
        [(True, False), (False, False), (False, False)],
    ]

    for bc1, bc2, bc3 in cases:
        comp = theano_code_(expr, broadcastables={x: bc1, y: bc2})
        assert comp.broadcastable == bc3

