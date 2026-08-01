
def test_invalid_repr():
    class MyRepr:
        def __repr__(self):
            raise AttributeError("Example error")

    with pytest.raises(TypeError):
        m.simple_bool_passthrough(MyRepr())

