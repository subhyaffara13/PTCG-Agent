
def test_raises_substitution():
    raises(ValueError, lambda: substitution([x**2 -1], []))
    raises(TypeError, lambda: substitution([x**2 -1]))
    raises(ValueError, lambda: substitution([x**2 -1], [sin(x)]))
    raises(TypeError, lambda: substitution([x**2 -1], x))
    raises(TypeError, lambda: substitution([x**2 -1], 1))

