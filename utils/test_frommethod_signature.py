
def test_frommethod_signature(fn, signature):
    assert str(inspect.signature(fn)) == signature

