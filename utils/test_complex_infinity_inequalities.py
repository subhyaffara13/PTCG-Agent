
def test_complex_infinity_inequalities():
    raises(TypeError, lambda: zoo > 0)
    raises(TypeError, lambda: zoo >= 0)
    raises(TypeError, lambda: zoo < 0)
    raises(TypeError, lambda: zoo <= 0)

