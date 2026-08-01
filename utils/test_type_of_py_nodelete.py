
def test_type_of_py_nodelete():
    # If the above test deleted the class, this will segfault
    assert m.get_type_of(m.DerivedClass1()) == m.DerivedClass1

