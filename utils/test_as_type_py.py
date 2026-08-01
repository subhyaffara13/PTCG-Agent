
def test_as_type_py():
    assert m.as_type(int) == int

    with pytest.raises(TypeError):
        assert m.as_type(1) == int

    with pytest.raises(TypeError):
        assert m.as_type(m.DerivedClass1()) == m.DerivedClass1

