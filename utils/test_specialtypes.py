
def test_specialtypes():
    assert dill.pickles(type(None))
    assert dill.pickles(type(NotImplemented))
    assert dill.pickles(type(Ellipsis))
    assert dill.pickles(type(EnumMeta))

