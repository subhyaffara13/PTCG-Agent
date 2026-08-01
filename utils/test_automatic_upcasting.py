
def test_automatic_upcasting():
    assert type(m.return_class_1()).__name__ == "DerivedClass1"
    assert type(m.return_class_2()).__name__ == "DerivedClass2"
    assert type(m.return_none()).__name__ == "NoneType"
    # Repeat these a few times in a random order to ensure no invalid caching is applied
    assert type(m.return_class_n(1)).__name__ == "DerivedClass1"
    assert type(m.return_class_n(2)).__name__ == "DerivedClass2"
    assert type(m.return_class_n(0)).__name__ == "BaseClass"
    assert type(m.return_class_n(2)).__name__ == "DerivedClass2"
    assert type(m.return_class_n(2)).__name__ == "DerivedClass2"
    assert type(m.return_class_n(0)).__name__ == "BaseClass"
    assert type(m.return_class_n(1)).__name__ == "DerivedClass1"

