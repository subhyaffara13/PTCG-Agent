
def test_Frac_postprocess():
    opt = {'frac': True}
    Frac.postprocess(opt)

    assert opt == {'frac': True}

