
def test_no_len():
    # there should be no len for numbers
    raises(TypeError, lambda: len(Rational(2)))
    raises(TypeError, lambda: len(Rational(2, 3)))
    raises(TypeError, lambda: len(Integer(2)))


def test_no_len():
    # there should be no len for numbers
    x = Symbol('x')
    raises(TypeError, lambda: len(x))

