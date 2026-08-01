
def test_none_deferred():
    """None passed as various argument types should defer to other overloads"""
    assert not m.defer_none_cstring("abc")
    assert m.defer_none_cstring(None)
    assert not m.defer_none_custom(UserType())
    assert m.defer_none_custom(None)
    assert m.nodefer_none_void(None)

