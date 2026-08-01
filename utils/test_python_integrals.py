
def test_python_integrals():
    # Simple
    f_1 = Integral(log(x), x)
    assert python(f_1) == "x = Symbol('x')\ne = Integral(log(x), x)"

    f_2 = Integral(x**2, x)
    assert python(f_2) == "x = Symbol('x')\ne = Integral(x**2, x)"

    # Double nesting of pow
    f_3 = Integral(x**(2**x), x)
    assert python(f_3) == "x = Symbol('x')\ne = Integral(x**(2**x), x)"

    # Definite integrals
    f_4 = Integral(x**2, (x, 1, 2))
    assert python(f_4) == "x = Symbol('x')\ne = Integral(x**2, (x, 1, 2))"

    f_5 = Integral(x**2, (x, Rational(1, 2), 10))
    assert python(
        f_5) == "x = Symbol('x')\ne = Integral(x**2, (x, Rational(1, 2), 10))"

    # Nested integrals
    f_6 = Integral(x**2*y**2, x, y)
    assert python(f_6) == "x = Symbol('x')\ny = Symbol('y')\ne = Integral(x**2*y**2, x, y)"

