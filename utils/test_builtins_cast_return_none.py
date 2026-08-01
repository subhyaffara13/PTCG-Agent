
def test_builtins_cast_return_none():
    """Casters produced with PYBIND11_TYPE_CASTER() should convert nullptr to None"""
    assert m.return_none_string() is None
    assert m.return_none_char() is None
    assert m.return_none_bool() is None
    assert m.return_none_int() is None
    assert m.return_none_float() is None
    assert m.return_none_pair() is None

