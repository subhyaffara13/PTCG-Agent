
def test_unhashable_exceptions(arg, func):
    class Unhashable:
        __hash__ = None

    with pytest.raises(TypeError) as exc_info:
        func(arg, Unhashable())
    assert "unhashable type:" in str(exc_info.value)

