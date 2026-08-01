
def test_trigonometric():
    n3 = Rational(3)
    e = (sin(x)**2).diff(x)
    assert e == 2*sin(x)*cos(x)
    e = e.subs(x, n3)
    assert e == 2*cos(n3)*sin(n3)

    e = (sin(x)**2).diff(x)
    assert e == 2*sin(x)*cos(x)
    e = e.subs(sin(x), cos(x))
    assert e == 2*cos(x)**2

    assert exp(pi).subs(exp, sin) == 0
    assert cos(exp(pi)).subs(exp, sin) == 1

    i = Symbol('i', integer=True)
    zoo = S.ComplexInfinity
    assert tan(x).subs(x, pi/2) is zoo
    assert cot(x).subs(x, pi) is zoo
    assert cot(i*x).subs(x, pi) is zoo
    assert tan(i*x).subs(x, pi/2) == tan(i*pi/2)
    assert tan(i*x).subs(x, pi/2).subs(i, 1) is zoo
    o = Symbol('o', odd=True)
    assert tan(o*x).subs(x, pi/2) == tan(o*pi/2)

