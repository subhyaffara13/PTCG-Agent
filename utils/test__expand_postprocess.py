
def test_Expand_postprocess():
    opt = {'expand': True}
    Expand.postprocess(opt)

    assert opt == {'expand': True}

