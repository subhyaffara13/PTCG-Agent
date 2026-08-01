
def test_load_external():
    """Load a `py::module_local` type that's only registered in an external module"""
    import pybind11_cross_module_tests as cm

    assert m.load_external1(cm.ExternalType1(11)) == 11
    assert m.load_external2(cm.ExternalType2(22)) == 22

    with pytest.raises(TypeError) as excinfo:
        assert m.load_external2(cm.ExternalType1(21)) == 21
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        assert m.load_external1(cm.ExternalType2(12)) == 12
    assert "incompatible function arguments" in str(excinfo.value)

