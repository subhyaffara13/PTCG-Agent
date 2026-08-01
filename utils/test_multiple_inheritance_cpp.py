
def test_multiple_inheritance_cpp():
    mt = m.MIType(3, 4)

    assert mt.foo() == 3
    assert mt.bar() == 4

