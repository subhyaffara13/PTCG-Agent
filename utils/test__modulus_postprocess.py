
def test_Modulus_postprocess():
    opt = {'modulus': 5}
    Modulus.postprocess(opt)

    assert opt == {
        'modulus': 5,
        'domain': FF(5),
    }

    opt = {'modulus': 5, 'symmetric': False}
    Modulus.postprocess(opt)

    assert opt == {
        'modulus': 5,
        'domain': FF(5, False),
        'symmetric': False,
    }

