
def test_attrdict():
    d = _idl.AttrDict({'one': 1})
    assert d['one'] == 1
    assert d.one == 1
    with pytest.raises(KeyError):
        d['two']
    with pytest.raises(AttributeError, match='has no attribute'):
        d.two

