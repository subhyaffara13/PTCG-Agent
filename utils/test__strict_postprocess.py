
def test_Strict_postprocess():
    opt = {'strict': True}
    Strict.postprocess(opt)

    assert opt == {'strict': True}

