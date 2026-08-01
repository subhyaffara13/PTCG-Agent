
def test_SAGE1():
    #see https://github.com/sympy/sympy/issues/3346
    class MyInt:
        def _sympy_(self):
            return Integer(5)
    m = MyInt()
    e = Rational(2)*m
    assert e == 10

    raises(TypeError, lambda: Rational(2)*MyInt)

