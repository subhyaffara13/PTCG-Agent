
def test_invert_real():
    x = Symbol('x', real=True)

    def ireal(x, s=S.Reals):
        return Intersection(s, x)

    assert invert_real(exp(x), z, x) == (x, ireal(FiniteSet(log(z))))

    y = Symbol('y', positive=True)
    n = Symbol('n', real=True)
    assert invert_real(x + 3, y, x) == (x, FiniteSet(y - 3))
    assert invert_real(x*3, y, x) == (x, FiniteSet(y / 3))

    assert invert_real(exp(x), y, x) == (x, FiniteSet(log(y)))
    assert invert_real(exp(3*x), y, x) == (x, FiniteSet(log(y) / 3))
    assert invert_real(exp(x + 3), y, x) == (x, FiniteSet(log(y) - 3))

    assert invert_real(exp(x) + 3, y, x) == (x, ireal(FiniteSet(log(y - 3))))
    assert invert_real(exp(x)*3, y, x) == (x, FiniteSet(log(y / 3)))

    assert invert_real(log(x), y, x) == (x, FiniteSet(exp(y)))
    assert invert_real(log(3*x), y, x) == (x, FiniteSet(exp(y) / 3))
    assert invert_real(log(x + 3), y, x) == (x, FiniteSet(exp(y) - 3))

    assert invert_real(Abs(x), y, x) == (x, FiniteSet(y, -y))

    assert invert_real(2**x, y, x) == (x, FiniteSet(log(y)/log(2)))
    assert invert_real(2**exp(x), y, x) == (x, ireal(FiniteSet(log(log(y)/log(2)))))

    assert invert_real(x**2, y, x) == (x, FiniteSet(sqrt(y), -sqrt(y)))
    assert invert_real(x**S.Half, y, x) == (x, FiniteSet(y**2))

    raises(ValueError, lambda: invert_real(x, x, x))

    # issue 21236
    assert invert_real(x**pi, y, x) == (x, FiniteSet(y**(1/pi)))
    assert invert_real(x**pi, -E, x) == (x, S.EmptySet)
    assert invert_real(x**Rational(3/2), 1000, x) == (x, FiniteSet(100))
    assert invert_real(x**1.0, 1, x) == (x**1.0, FiniteSet(1))

    raises(ValueError, lambda: invert_real(S.One, y, x))

    assert invert_real(x**31 + x, y, x) == (x**31 + x, FiniteSet(y))

    lhs = x**31 + x
    base_values =  FiniteSet(y - 1, -y - 1)
    assert invert_real(Abs(x**31 + x + 1), y, x) == (lhs, base_values)

    assert dumeq(invert_real(sin(x), y, x), (x,
        ConditionSet(x, (S(-1) <= y) & (y <= S(1)), Union(
            ImageSet(Lambda(n, 2*n*pi + asin(y)), S.Integers),
            ImageSet(Lambda(n, pi*2*n + pi - asin(y)), S.Integers)))))

    assert dumeq(invert_real(sin(exp(x)), y, x), (x,
        ConditionSet(x, (S(-1) <= y) & (y <= S(1)), Union(
            ImageSet(Lambda(n, log(2*n*pi + asin(y))), S.Integers),
            ImageSet(Lambda(n, log(pi*2*n + pi - asin(y))), S.Integers)))))

    assert dumeq(invert_real(csc(x), y, x), (x,
        ConditionSet(x, ((S(1) <= y) & (y < oo)) | ((-oo < y) & (y <= S(-1))),
            Union(ImageSet(Lambda(n, 2*n*pi + acsc(y)), S.Integers),
                ImageSet(Lambda(n, 2*n*pi - acsc(y) + pi), S.Integers)))))

    assert dumeq(invert_real(csc(exp(x)), y, x), (x,
        ConditionSet(x, ((S(1) <= y) & (y < oo)) | ((-oo < y) & (y <= S(-1))),
            Union(ImageSet(Lambda(n, log(2*n*pi + acsc(y))), S.Integers),
                ImageSet(Lambda(n, log(2*n*pi - acsc(y) + pi)), S.Integers)))))

    assert dumeq(invert_real(cos(x), y, x), (x,
        ConditionSet(x, (S(-1) <= y) & (y <= S(1)), Union(
            ImageSet(Lambda(n, 2*n*pi + acos(y)), S.Integers),
            ImageSet(Lambda(n, 2*n*pi - acos(y)), S.Integers)))))

    assert dumeq(invert_real(cos(exp(x)), y, x), (x,
        ConditionSet(x, (S(-1) <= y) & (y <= S(1)), Union(
            ImageSet(Lambda(n, log(2*n*pi + acos(y))), S.Integers),
            ImageSet(Lambda(n, log(2*n*pi - acos(y))), S.Integers)))))

    assert dumeq(invert_real(sec(x), y, x), (x,
        ConditionSet(x, ((S(1) <= y) & (y < oo)) | ((-oo < y) & (y <= S(-1))),
            Union(ImageSet(Lambda(n, 2*n*pi + asec(y)), S.Integers), \
                ImageSet(Lambda(n, 2*n*pi - asec(y)), S.Integers)))))

    assert dumeq(invert_real(sec(exp(x)), y, x), (x,
        ConditionSet(x, ((S(1) <= y) & (y < oo)) | ((-oo < y) & (y <= S(-1))),
            Union(ImageSet(Lambda(n, log(2*n*pi - asec(y))), S.Integers),
                ImageSet(Lambda(n, log(2*n*pi + asec(y))), S.Integers)))))

    assert dumeq(invert_real(tan(x), y, x), (x,
        ConditionSet(x, (-oo < y) & (y < oo),
            ImageSet(Lambda(n, n*pi + atan(y)), S.Integers))))

    assert dumeq(invert_real(tan(exp(x)), y, x), (x,
        ConditionSet(x, (-oo < y) & (y < oo),
            ImageSet(Lambda(n, log(n*pi + atan(y))), S.Integers))))

    assert dumeq(invert_real(cot(x), y, x), (x,
        ConditionSet(x, (-oo < y) & (y < oo),
            ImageSet(Lambda(n, n*pi + acot(y)), S.Integers))))

    assert dumeq(invert_real(cot(exp(x)), y, x), (x,
        ConditionSet(x, (-oo < y) & (y < oo),
            ImageSet(Lambda(n, log(n*pi + acot(y))), S.Integers))))

    assert dumeq(invert_real(tan(tan(x)), y, x),
        (x, ConditionSet(x, Eq(tan(tan(x)), y), S.Reals)))
        # slight regression compared to previous result:
        # (tan(x), imageset(Lambda(n, n*pi + atan(y)), S.Integers)))

    x = Symbol('x', positive=True)
    assert invert_real(x**pi, y, x) == (x, FiniteSet(y**(1/pi)))

    r = Symbol('r', real=True)
    p = Symbol('p', positive=True)
    assert invert_real(sinh(x), r, x) == (x, FiniteSet(asinh(r)))
    assert invert_real(sinh(log(x)), p, x) == (x, FiniteSet(exp(asinh(p))))

    assert invert_real(cosh(x), r, x) == (x, Intersection(
        FiniteSet(-acosh(r), acosh(r)), S.Reals))
    assert invert_real(cosh(x), p + 1, x) == (x,
        FiniteSet(-acosh(p + 1), acosh(p + 1)))

    assert invert_real(tanh(x), r, x) == (x, Intersection(FiniteSet(atanh(r)), S.Reals))
    assert invert_real(coth(x), p+1, x) == (x, FiniteSet(acoth(p+1)))
    assert invert_real(sech(x), r, x) == (x, Intersection(
        FiniteSet(-asech(r), asech(r)), S.Reals))
    assert invert_real(csch(x), p, x) == (x, FiniteSet(acsch(p)))

    assert dumeq(invert_real(tanh(sin(x)), r, x), (x,
        ConditionSet(x, (S(-1) <= atanh(r)) & (atanh(r) <= S(1)), Union(
            ImageSet(Lambda(n, 2*n*pi + asin(atanh(r))), S.Integers),
            ImageSet(Lambda(n, 2*n*pi - asin(atanh(r)) + pi), S.Integers)))))

