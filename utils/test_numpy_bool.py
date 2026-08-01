
def test_numpy_bool():
    np = pytest.importorskip("numpy")

    convert, noconvert = m.bool_passthrough, m.bool_passthrough_noconvert

    def cant_convert(v):
        pytest.raises(TypeError, convert, v)

    # np.bool_ is not considered implicit
    assert convert(np.bool_(True)) is True
    assert convert(np.bool_(False)) is False
    assert noconvert(np.bool_(True)) is True
    assert noconvert(np.bool_(False)) is False
    cant_convert(np.zeros(2, dtype="int"))

