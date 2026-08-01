
def test_Wrt_postprocess():
    opt = {'wrt': ['x']}
    Wrt.postprocess(opt)

    assert opt == {'wrt': ['x']}

