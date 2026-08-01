
def test_All_postprocess():
    opt = {'all': True}
    All.postprocess(opt)

    assert opt == {'all': True}

