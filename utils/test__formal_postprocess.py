
def test_Formal_postprocess():
    opt = {'formal': True}
    Formal.postprocess(opt)

    assert opt == {'formal': True}

