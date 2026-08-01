
def test_void_caster():
    assert m.load_nullptr_t(None) is None
    assert m.cast_nullptr_t() is None

