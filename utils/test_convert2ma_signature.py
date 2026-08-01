
def test_convert2ma_signature(fn, signature):
    assert str(inspect.signature(fn)) == signature
    assert fn.__module__ == 'numpy.ma.core'

