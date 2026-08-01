
def test_type_of_py():
    assert m.get_type_of(1) == int
    assert m.get_type_of(m.DerivedClass1()) == m.DerivedClass1
    assert m.get_type_of(int) == type

