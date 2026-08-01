
def test_function_overloading():
    assert m.test_function() == "test_function()"
    assert m.test_function(7) == "test_function(7)"
    assert m.test_function(m.MyEnum.EFirstEntry) == "test_function(enum=1)"
    assert m.test_function(m.MyEnum.ESecondEntry) == "test_function(enum=2)"

    assert m.test_function() == "test_function()"
    assert m.test_function("abcd") == "test_function(char *)"
    assert m.test_function(1, 1.0) == "test_function(int, float)"
    assert m.test_function(1, 1.0) == "test_function(int, float)"
    assert m.test_function(2.0, 2) == "test_function(float, int)"

