
def test_constructor_no_levels():
    msg = "non-zero number of levels/codes"
    with pytest.raises(ValueError, match=msg):
        MultiIndex(levels=[], codes=[])

    msg = "Must pass both levels and codes"
    with pytest.raises(TypeError, match=msg):
        MultiIndex(levels=[])
    with pytest.raises(TypeError, match=msg):
        MultiIndex(codes=[])

