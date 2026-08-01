
def test_Gen_postprocess():
    opt = {'gen': x}
    Gen.postprocess(opt)

    assert opt == {'gen': x}

