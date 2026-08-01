
def test_Symbols_postprocess():
    opt = {'symbols': [x, y, z]}
    Symbols.postprocess(opt)

    assert opt == {'symbols': [x, y, z]}

