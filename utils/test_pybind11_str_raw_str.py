
def test_pybind11_str_raw_str():
    # specifically to exercise pybind11::str::raw_str
    cvt = m.convert_to_pybind11_str
    assert cvt("Str") == "Str"
    assert cvt(b"Bytes") == "b'Bytes'"
    assert cvt(None) == "None"
    assert cvt(False) == "False"
    assert cvt(True) == "True"
    assert cvt(42) == "42"
    assert cvt(2**65) == "36893488147419103232"
    assert cvt(-1.50) == "-1.5"
    assert cvt(()) == "()"
    assert cvt((18,)) == "(18,)"
    assert cvt([]) == "[]"
    assert cvt([28]) == "[28]"
    assert cvt({}) == "{}"
    assert cvt({3: 4}) == "{3: 4}"
    assert cvt(set()) == "set()"
    assert cvt({3}) == "{3}"

    valid_orig = "Ǳ"
    valid_utf8 = valid_orig.encode("utf-8")
    valid_cvt = cvt(valid_utf8)
    if hasattr(m, "PYBIND11_STR_LEGACY_PERMISSIVE"):
        assert valid_cvt is valid_utf8
    else:
        assert type(valid_cvt) is str
        assert valid_cvt == "b'\\xc7\\xb1'"

    malformed_utf8 = b"\x80"
    if hasattr(m, "PYBIND11_STR_LEGACY_PERMISSIVE"):
        assert cvt(malformed_utf8) is malformed_utf8
    else:
        malformed_cvt = cvt(malformed_utf8)
        assert type(malformed_cvt) is str
        assert malformed_cvt == "b'\\x80'"

