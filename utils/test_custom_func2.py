
def test_custom_func2():
    assert m.custom_function2(3) == 27
    assert m.roundtrip(m.custom_function2)(3) == 27

