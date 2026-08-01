
def test_integer_integer_comparison(comp):
    # Test that the NumPy comparison ufuncs work with large Python integers
    assert comp(2**200, -2**200) == comp(2**200, -2**200, dtype=object)

