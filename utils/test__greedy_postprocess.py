
def test_Greedy_postprocess():
    opt = {'greedy': True}
    Greedy.postprocess(opt)

    assert opt == {'greedy': True}

