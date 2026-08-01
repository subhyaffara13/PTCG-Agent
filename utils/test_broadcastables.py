
def test_broadcastables():
    """ Test the "broadcastables" argument when printing symbol-like objects. """

    # No restrictions on shape
    for s in [x, f_t]:
        for bc in [(), (False,), (True,), (False, False), (True, False)]:
            assert aesara_code_(s, broadcastables={s: bc}).broadcastable == bc


def test_broadcastables():
    """ Test the "broadcastables" argument when printing symbol-like objects. """

    # No restrictions on shape
    for s in [x, f_t]:
        for bc in [(), (False,), (True,), (False, False), (True, False)]:
            assert theano_code_(s, broadcastables={s: bc}).broadcastable == bc

