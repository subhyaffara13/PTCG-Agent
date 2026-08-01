
def test_pass_bytes_or_unicode_to_string_types():
    assert m.pass_to_pybind11_bytes(b"Bytes") == 5
    with pytest.raises(TypeError):
        m.pass_to_pybind11_bytes("Str")

    if hasattr(m, "PYBIND11_STR_LEGACY_PERMISSIVE"):
        assert m.pass_to_pybind11_str(b"Bytes") == 5
    else:
        with pytest.raises(TypeError):
            m.pass_to_pybind11_str(b"Bytes")
    assert m.pass_to_pybind11_str("Str") == 3

    assert m.pass_to_std_string(b"Bytes") == 5
    assert m.pass_to_std_string("Str") == 3

    malformed_utf8 = b"\x80"
    if hasattr(m, "PYBIND11_STR_LEGACY_PERMISSIVE"):
        assert m.pass_to_pybind11_str(malformed_utf8) == 1
    else:
        with pytest.raises(TypeError):
            m.pass_to_pybind11_str(malformed_utf8)

