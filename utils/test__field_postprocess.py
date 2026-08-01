
def test_Field_postprocess():
    opt = {'field': True}
    Field.postprocess(opt)

    assert opt == {'field': True}

