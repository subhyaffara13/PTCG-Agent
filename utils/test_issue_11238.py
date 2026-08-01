
def test_issue_11238():
    from sympy.geometry.point import Point
    xx = 8*tan(pi*Rational(13, 45))/(tan(pi*Rational(13, 45)) + sqrt(3))
    yy = (-8*sqrt(3)*tan(pi*Rational(13, 45))**2 + 24*tan(pi*Rational(13, 45)))/(-3 + tan(pi*Rational(13, 45))**2)
    p1 = Point(0, 0)
    p2 = Point(1, -sqrt(3))
    p0 = Point(xx,yy)
    m1 = Matrix([p1 - simplify(p0), p2 - simplify(p0)])
    m2 = Matrix([p1 - p0, p2 - p0])
    m3 = Matrix([simplify(p1 - p0), simplify(p2 - p0)])

    # This system has expressions which are zero and
    # cannot be easily proved to be such, so without
    # numerical testing, these assertions will fail.
    Z = lambda x: abs(x.n()) < 1e-20
    assert m1.rank(simplify=True, iszerofunc=Z) == 1
    assert m2.rank(simplify=True, iszerofunc=Z) == 1
    assert m3.rank(simplify=True, iszerofunc=Z) == 1


def test_issue_11238():
    from sympy.geometry.point import Point
    xx = 8*tan(pi*Rational(13, 45))/(tan(pi*Rational(13, 45)) + sqrt(3))
    yy = (-8*sqrt(3)*tan(pi*Rational(13, 45))**2 + 24*tan(pi*Rational(13, 45)))/(-3 + tan(pi*Rational(13, 45))**2)
    p1 = Point(0, 0)
    p2 = Point(1, -sqrt(3))
    p0 = Point(xx,yy)
    m1 = Matrix([p1 - simplify(p0), p2 - simplify(p0)])
    m2 = Matrix([p1 - p0, p2 - p0])
    m3 = Matrix([simplify(p1 - p0), simplify(p2 - p0)])

    # This system has expressions which are zero and
    # cannot be easily proved to be such, so without
    # numerical testing, these assertions will fail.
    Z = lambda x: abs(x.n()) < 1e-20
    assert m1.rank(simplify=True, iszerofunc=Z) == 1
    assert m2.rank(simplify=True, iszerofunc=Z) == 1
    assert m3.rank(simplify=True, iszerofunc=Z) == 1

