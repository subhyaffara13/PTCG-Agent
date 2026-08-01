
def test_integer_casting():
    """Issue #929 - out-of-range integer values shouldn't be accepted"""
    assert m.i32_str(-1) == "-1"
    assert m.i64_str(-1) == "-1"
    assert m.i32_str(2000000000) == "2000000000"
    assert m.u32_str(2000000000) == "2000000000"
    assert m.i64_str(-999999999999) == "-999999999999"
    assert m.u64_str(999999999999) == "999999999999"

    with pytest.raises(TypeError) as excinfo:
        m.u32_str(-1)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.u64_str(-1)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.i32_str(-3000000000)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.i32_str(3000000000)
    assert "incompatible function arguments" in str(excinfo.value)

