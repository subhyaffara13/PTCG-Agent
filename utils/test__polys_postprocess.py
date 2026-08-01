
def test_Polys_postprocess():
    opt = {'polys': True}
    Polys.postprocess(opt)

    assert opt == {'polys': True}

