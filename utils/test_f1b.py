
def test_f1b():
    m = Symbol("m")
    n = Symbol("n")
    h = Symbol("h")
    a = Symbol("a")
    assert limit(sin(x)/x, x, 2) == sin(2)/2  # 216a
    assert limit(sin(3*x)/x, x, 0) == 3  # 217
    assert limit(sin(5*x)/sin(2*x), x, 0) == Rational(5, 2)  # 218
    assert limit(sin(pi*x)/sin(3*pi*x), x, 0) == Rational(1, 3)  # 219
    assert limit(x*sin(pi/x), x, oo) == pi  # 220
    assert limit((1 - cos(x))/x**2, x, 0) == S.Half  # 221
    assert limit(x*sin(1/x), x, oo) == 1  # 227b
    assert limit((cos(m*x) - cos(n*x))/x**2, x, 0) == -m**2/2 + n**2/2  # 232
    assert limit((tan(x) - sin(x))/x**3, x, 0) == S.Half  # 233
    assert limit((x - sin(2*x))/(x + sin(3*x)), x, 0) == -Rational(1, 4)  # 237
    assert limit((1 - sqrt(cos(x)))/x**2, x, 0) == Rational(1, 4)  # 239
    assert limit((sqrt(1 + sin(x)) - sqrt(1 - sin(x)))/x, x, 0) == 1  # 240

    assert limit((1 + h/x)**x, x, oo) == exp(h)  # Primer 9
    assert limit((sin(x) - sin(a))/(x - a), x, a) == cos(a)  # 222, *176
    assert limit((cos(x) - cos(a))/(x - a), x, a) == -sin(a)  # 223
    assert limit((sin(x + h) - sin(x))/h, h, 0) == cos(x)  # 225

