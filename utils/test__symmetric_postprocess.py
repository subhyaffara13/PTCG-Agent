
def test_Symmetric_postprocess():
    opt = {'symmetric': True}
    Symmetric.postprocess(opt)

    assert opt == {'symmetric': True}

