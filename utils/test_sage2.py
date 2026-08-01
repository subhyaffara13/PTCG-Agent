
def test_SAGE2():
    class MyInt:
        def __int__(self):
            return 5
    assert sympify(MyInt()) == 5
    e = Rational(2)*MyInt()
    assert e == 10

    raises(TypeError, lambda: Rational(2)*MyInt)

