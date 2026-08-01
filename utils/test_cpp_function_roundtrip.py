
def test_cpp_function_roundtrip():
    """Test if passing a function pointer from C++ -> Python -> C++ yields the original pointer"""

    assert (
        m.test_dummy_function(m.dummy_function) == "matches dummy_function: eval(1) = 2"
    )
    assert (
        m.test_dummy_function(m.roundtrip(m.dummy_function))
        == "matches dummy_function: eval(1) = 2"
    )
    assert (
        m.test_dummy_function(m.dummy_function_overloaded)
        == "matches dummy_function: eval(1) = 2"
    )
    assert m.roundtrip(None, expect_none=True) is None
    assert (
        m.test_dummy_function(lambda x: x + 2)
        == "can't convert to function pointer: eval(1) = 3"
    )

    with pytest.raises(TypeError) as excinfo:
        m.test_dummy_function(m.dummy_function2)
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        m.test_dummy_function(lambda x, y: x + y)
    assert any(
        s in str(excinfo.value)
        for s in ("missing 1 required positional argument", "takes exactly 2 arguments")
    )

