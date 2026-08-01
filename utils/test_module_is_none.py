
def test_module_is_none():
    assert obj.__module__ is None
    assert dill.copy(obj)(3) == obj(3)

