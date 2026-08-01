
def test_Auto_postprocess():
    opt = {'auto': True}
    Auto.postprocess(opt)

    assert opt == {'auto': True}

