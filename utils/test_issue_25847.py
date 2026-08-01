
def test_issue_25847():
    #atan
    assert limit(atan(sin(x)/x), x, 0, '+-') == pi/4
    assert limit(atan(exp(1/x)), x, 0, '+') == pi/2
    assert limit(atan(exp(1/x)), x, 0, '-') == 0

    #asin
    assert limit(asin(sin(x)/x), x, 0, '+-') == pi/2
    assert limit(asin(exp(1/x)), x, 0, '+') == -oo*I
    assert limit(asin(exp(1/x)), x, 0, '-') == 0

    #acos
    assert limit(acos(sin(x)/x), x, 0, '+-') == 0
    assert limit(acos(exp(1/x)), x, 0, '+') == oo*I
    assert limit(acos(exp(1/x)), x, 0, '-') == pi/2

    #acot
    assert limit(acot(sin(x)/x), x, 0, '+-') == pi/4
    assert limit(acot(exp(1/x)), x, 0, '+') == 0
    assert limit(acot(exp(1/x)), x, 0, '-') == pi/2

    #asec
    assert limit(asec(sin(x)/x), x, 0, '+-') == 0
    assert limit(asec(exp(1/x)), x, 0, '+') == pi/2
    assert limit(asec(exp(1/x)), x, 0, '-') == oo*I

    #acsc
    assert limit(acsc(sin(x)/x), x, 0, '+-') == pi/2
    assert limit(acsc(exp(1/x)), x, 0, '+') == 0
    assert limit(acsc(exp(1/x)), x, 0, '-') == -oo*I

    #atanh
    assert limit(atanh(sin(x)/x), x, 0, '+-') == oo
    assert limit(atanh(exp(1/x)), x, 0, '+') == -I*pi/2
    assert limit(atanh(exp(1/x)), x, 0, '-') == 0

    #asinh
    assert limit(asinh(sin(x)/x), x, 0, '+-') == log(1 + sqrt(2))
    assert limit(asinh(exp(1/x)), x, 0, '+') == oo
    assert limit(asinh(exp(1/x)), x, 0, '-') == 0

    #acosh
    assert limit(acosh(sin(x)/x), x, 0, '+-') == 0
    assert limit(acosh(exp(1/x)), x, 0, '+') == oo
    assert limit(acosh(exp(1/x)), x, 0, '-') == I*pi/2

    #acoth
    assert limit(acoth(sin(x)/x), x, 0, '+-') == oo
    assert limit(acoth(exp(1/x)), x, 0, '+') == 0
    assert limit(acoth(exp(1/x)), x, 0, '-') == -I*pi/2

    #asech
    assert limit(asech(sin(x)/x), x, 0, '+-') == 0
    assert limit(asech(exp(1/x)), x, 0, '+') == I*pi/2
    assert limit(asech(exp(1/x)), x, 0, '-') == oo

    #acsch
    assert limit(acsch(sin(x)/x), x, 0, '+-') == log(1 + sqrt(2))
    assert limit(acsch(exp(1/x)), x, 0, '+') == 0
    assert limit(acsch(exp(1/x)), x, 0, '-') == oo


def test_issue_25847():
    x = Symbol('x')

    #atanh
    assert atanh(sin(x)/x).as_leading_term(x) == atanh(sin(x)/x)
    raises(PoleError, lambda: atanh(exp(1/x)).as_leading_term(x))

    #asinh
    assert asinh(sin(x)/x).as_leading_term(x) == log(1 + sqrt(2))
    raises(PoleError, lambda: asinh(exp(1/x)).as_leading_term(x))

    #acosh
    assert acosh(sin(x)/x).as_leading_term(x) == 0
    raises(PoleError, lambda: acosh(exp(1/x)).as_leading_term(x))

    #acoth
    assert acoth(sin(x)/x).as_leading_term(x) == acoth(sin(x)/x)
    raises(PoleError, lambda: acoth(exp(1/x)).as_leading_term(x))

    #asech
    assert asech(sinh(x)/x).as_leading_term(x) == 0
    raises(PoleError, lambda: asech(exp(1/x)).as_leading_term(x))

    #acsch
    assert acsch(sin(x)/x).as_leading_term(x) == log(1 + sqrt(2))
    raises(PoleError, lambda: acsch(exp(1/x)).as_leading_term(x))


def test_issue_25847():
    #atan
    assert atan(sin(x)/x).as_leading_term(x) == pi/4
    raises(PoleError, lambda: atan(exp(1/x)).as_leading_term(x))

    #asin
    assert asin(sin(x)/x).as_leading_term(x) == pi/2
    raises(PoleError, lambda: asin(exp(1/x)).as_leading_term(x))

    #acos
    assert acos(sin(x)/x).as_leading_term(x) == 0
    raises(PoleError, lambda: acos(exp(1/x)).as_leading_term(x))

    #acot
    assert acot(sin(x)/x).as_leading_term(x) == pi/4
    raises(PoleError, lambda: acot(exp(1/x)).as_leading_term(x))

    #asec
    assert asec(sin(x)/x).as_leading_term(x) == 0
    raises(PoleError, lambda: asec(exp(1/x)).as_leading_term(x))

    #acsc
    assert acsc(sin(x)/x).as_leading_term(x) == pi/2
    raises(PoleError, lambda: acsc(exp(1/x)).as_leading_term(x))

