
def test_Include_postprocess():
    opt = {'include': True}
    Include.postprocess(opt)

    assert opt == {'include': True}

