
def test_isinstance_string_types():
    assert m.isinstance_pybind11_bytes(b"")
    assert not m.isinstance_pybind11_bytes("")

    assert m.isinstance_pybind11_str("")
    if hasattr(m, "PYBIND11_STR_LEGACY_PERMISSIVE"):
        assert m.isinstance_pybind11_str(b"")
    else:
        assert not m.isinstance_pybind11_str(b"")

