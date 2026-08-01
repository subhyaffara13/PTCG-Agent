
def test_Method_postprocess():
    opt = {'method': 'f5b'}
    Method.postprocess(opt)

    assert opt == {'method': 'f5b'}

