
def test_overload_ordering():
    "Check to see if the normal overload order (first defined) and prepend overload order works"
    assert m.overload_order("string") == 1
    assert m.overload_order(0) == 4

    assert "1. overload_order(arg0: int) -> int" in m.overload_order.__doc__
    assert "2. overload_order(arg0: str) -> int" in m.overload_order.__doc__
    assert "3. overload_order(arg0: str) -> int" in m.overload_order.__doc__
    assert "4. overload_order(arg0: int) -> int" in m.overload_order.__doc__

    with pytest.raises(TypeError) as err:
        m.overload_order(1.1)

    assert "1. (arg0: int) -> int" in str(err.value)
    assert "2. (arg0: str) -> int" in str(err.value)
    assert "3. (arg0: str) -> int" in str(err.value)
    assert "4. (arg0: int) -> int" in str(err.value)

