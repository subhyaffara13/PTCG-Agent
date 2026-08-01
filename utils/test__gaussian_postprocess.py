
def test_Gaussian_postprocess():
    opt = {'gaussian': True}
    Gaussian.postprocess(opt)

    assert opt == {
        'gaussian': True,
        'domain': QQ_I,
    }

