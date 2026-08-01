
def test_Gens_postprocess():
    opt = {'gens': (x, y)}
    Gens.postprocess(opt)

    assert opt == {'gens': (x, y)}

