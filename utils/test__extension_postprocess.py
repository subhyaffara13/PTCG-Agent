
def test_Extension_postprocess():
    opt = {'extension': {sqrt(2)}}
    Extension.postprocess(opt)

    assert opt == {
        'extension': {sqrt(2)},
        'domain': QQ.algebraic_field(sqrt(2)),
    }

    opt = {'extension': True}
    Extension.postprocess(opt)

    assert opt == {'extension': True}

