
def test_python_basic():
    # Simple numbers/symbols
    assert python(-Rational(1)/2) == "e = Rational(-1, 2)"
    assert python(-Rational(13)/22) == "e = Rational(-13, 22)"
    assert python(oo) == "e = oo"

    # Powers
    assert python(x**2) == "x = Symbol(\'x\')\ne = x**2"
    assert python(1/x) == "x = Symbol('x')\ne = 1/x"
    assert python(y*x**-2) == "y = Symbol('y')\nx = Symbol('x')\ne = y/x**2"
    assert python(
        x**Rational(-5, 2)) == "x = Symbol('x')\ne = x**Rational(-5, 2)"

    # Sums of terms
    assert python(x**2 + x + 1) in [
        "x = Symbol('x')\ne = 1 + x + x**2",
        "x = Symbol('x')\ne = x + x**2 + 1",
        "x = Symbol('x')\ne = x**2 + x + 1", ]
    assert python(1 - x) in [
        "x = Symbol('x')\ne = 1 - x",
        "x = Symbol('x')\ne = -x + 1"]
    assert python(1 - 2*x) in [
        "x = Symbol('x')\ne = 1 - 2*x",
        "x = Symbol('x')\ne = -2*x + 1"]
    assert python(1 - Rational(3, 2)*y/x) in [
        "y = Symbol('y')\nx = Symbol('x')\ne = 1 - 3/2*y/x",
        "y = Symbol('y')\nx = Symbol('x')\ne = -3/2*y/x + 1",
        "y = Symbol('y')\nx = Symbol('x')\ne = 1 - 3*y/(2*x)"]

    # Multiplication
    assert python(x/y) == "x = Symbol('x')\ny = Symbol('y')\ne = x/y"
    assert python(-x/y) == "x = Symbol('x')\ny = Symbol('y')\ne = -x/y"
    assert python((x + 2)/y) in [
        "y = Symbol('y')\nx = Symbol('x')\ne = 1/y*(2 + x)",
        "y = Symbol('y')\nx = Symbol('x')\ne = 1/y*(x + 2)",
        "x = Symbol('x')\ny = Symbol('y')\ne = 1/y*(2 + x)",
        "x = Symbol('x')\ny = Symbol('y')\ne = (2 + x)/y",
        "x = Symbol('x')\ny = Symbol('y')\ne = (x + 2)/y"]
    assert python((1 + x)*y) in [
        "y = Symbol('y')\nx = Symbol('x')\ne = y*(1 + x)",
        "y = Symbol('y')\nx = Symbol('x')\ne = y*(x + 1)", ]

    # Check for proper placement of negative sign
    assert python(-5*x/(x + 10)) == "x = Symbol('x')\ne = -5*x/(x + 10)"
    assert python(1 - Rational(3, 2)*(x + 1)) in [
        "x = Symbol('x')\ne = Rational(-3, 2)*x + Rational(-1, 2)",
        "x = Symbol('x')\ne = -3*x/2 + Rational(-1, 2)",
        "x = Symbol('x')\ne = -3*x/2 + Rational(-1, 2)"
    ]

