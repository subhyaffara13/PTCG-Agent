
def test_font_path():
    fp = FontPath('foo', 123)
    fp2 = FontPath('foo', 321)
    assert str(fp) == 'foo'
    assert repr(fp) == "FontPath('foo', 123)"
    assert fp.path == 'foo'
    assert fp.face_index == 123
    # Should be immutable.
    with pytest.raises(AttributeError, match='has no setter'):
        fp.path = 'bar'
    with pytest.raises(AttributeError, match='has no setter'):
        fp.face_index = 321
    # Should be comparable with str and itself.
    assert fp == 'foo'
    assert fp == FontPath('foo', 123)
    assert fp <= fp
    assert fp >= fp
    assert fp != fp2
    assert fp < fp2
    assert fp <= fp2
    assert fp2 > fp
    assert fp2 >= fp
    # Should be hashable, but not the same as str.
    d = {fp: 1, 'bar': 2}
    assert fp in d
    assert d[fp] == 1
    assert d[FontPath('foo', 123)] == 1
    assert fp2 not in d
    assert 'foo' not in d
    assert FontPath('bar', 0) not in d

