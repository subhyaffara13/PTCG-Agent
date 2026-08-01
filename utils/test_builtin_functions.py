
def test_builtin_functions():
    assert m.get_len(list(range(42))) == 42
    with pytest.raises(TypeError) as exc_info:
        m.get_len(i for i in range(42))
    assert str(exc_info.value) in [
        "object of type 'generator' has no len()",
        "'generator' has no length",
    ]  # PyPy

