
def test_Order_postprocess():
    opt = {'order': True}
    Order.postprocess(opt)

    assert opt == {'order': True}

