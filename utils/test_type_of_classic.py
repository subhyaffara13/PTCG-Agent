
def test_type_of_classic():
    assert m.get_type_classic(1) == int
    assert m.get_type_classic(m.DerivedClass1()) == m.DerivedClass1
    assert m.get_type_classic(int) == type

