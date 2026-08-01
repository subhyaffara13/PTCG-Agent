
def test_Sort_postprocess():
    opt = {'sort': 'x > y'}
    Sort.postprocess(opt)

    assert opt == {'sort': 'x > y'}

