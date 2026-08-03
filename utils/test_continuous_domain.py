from typing import Union

def test_continuous_domain():
    assert continuous_domain(sin(x), x, Interval(0, 2*pi)) == Interval(0, 2*pi)
    assert continuous_domain(tan(x), x, Interval(0, 2*pi)) == \
        Union(Interval(0, pi/2, False, True), Interval(pi/2, pi*Rational(3, 2), True, True),
              Interval(pi*Rational(3, 2), 2*pi, True, False))
    assert continuous_domain(cot(x), x, Interval(0, 2*pi)) == Union(
        Interval.open(0, pi), Interval.open(pi, 2*pi))
    assert continuous_domain((x - 1)/((x - 1)**2), x, S.Reals) == \
        Union(Interval(-oo, 1, True, True), Interval(1, oo, True, True))
    assert continuous_domain(log(x) + log(4*x - 1), x, S.Reals) == \
        Interval(Rational(1, 4), oo, True, True)
    assert continuous_domain(1/sqrt(x - 3), x, S.Reals) == Interval(3, oo, True, True)
    assert continuous_domain(1/x - 2, x, S.Reals) == \
        Union(Interval.open(-oo, 0), Interval.open(0, oo))
    assert continuous_domain(1/(x**2 - 4) + 2, x, S.Reals) == \
        Union(Interval.open(-oo, -2), Interval.open(-2, 2), Interval.open(2, oo))
    assert continuous_domain((x+1)**pi, x, S.Reals) == Interval(-1, oo)
    assert continuous_domain((x+1)**(pi/2), x, S.Reals) == Interval(-1, oo)
    assert continuous_domain(x**x, x, S.Reals) == Interval(0, oo)
    assert continuous_domain((x+1)**log(x**2), x, S.Reals) == Union(
        Interval.Ropen(-1, 0), Interval.open(0, oo))
    domain = continuous_domain(log(tan(x)**2 + 1), x, S.Reals)
    assert not domain.contains(3*pi/2)
    assert domain.contains(5)
    d = Symbol('d', even=True, zero=False)
    assert continuous_domain(x**(1/d), x, S.Reals) == Interval(0, oo)
    n = Dummy('n')
    assert continuous_domain(1/sin(x), x, S.Reals).dummy_eq(Complement(
        S.Reals, Union(ImageSet(Lambda(n, 2*n*pi + pi), S.Integers),
                       ImageSet(Lambda(n, 2*n*pi), S.Integers))))
    assert continuous_domain(sin(x) + cos(x), x, S.Reals) == S.Reals
    assert continuous_domain(asin(x), x, S.Reals) == Interval(-1, 1) # issue #21786
    assert continuous_domain(1/acos(log(x)), x, S.Reals) == Interval.Ropen(exp(-1), E)
    assert continuous_domain(sinh(x)+cosh(x), x, S.Reals) == S.Reals
    assert continuous_domain(tanh(x)+sech(x), x, S.Reals) == S.Reals
    assert continuous_domain(atan(x)+asinh(x), x, S.Reals) == S.Reals
    assert continuous_domain(acosh(x), x, S.Reals) == Interval(1, oo)
    assert continuous_domain(atanh(x), x, S.Reals) == Interval.open(-1, 1)
    assert continuous_domain(atanh(x)+acosh(x), x, S.Reals) == S.EmptySet
    assert continuous_domain(asech(x), x, S.Reals) == Interval.Lopen(0, 1)
    assert continuous_domain(acoth(x), x, S.Reals) == Union(
        Interval.open(-oo, -1), Interval.open(1, oo))
    assert continuous_domain(asec(x), x, S.Reals) == Union(
        Interval(-oo, -1), Interval(1, oo))
    assert continuous_domain(acsc(x), x, S.Reals) == Union(
        Interval(-oo, -1), Interval(1, oo))
    for f in (coth, acsch, csch):
        assert continuous_domain(f(x), x, S.Reals) == Union(
            Interval.open(-oo, 0), Interval.open(0, oo))
    assert continuous_domain(acot(x), x, S.Reals).contains(0) == False
    assert continuous_domain(1/(exp(x) - x), x, S.Reals) == Complement(
        S.Reals, ConditionSet(x, Eq(-x + exp(x), 0), S.Reals))
    assert continuous_domain(frac(x**2), x, Interval(-2,-1)) == Union(
        Interval.open(-2, -sqrt(3)), Interval.open(-sqrt(2), -1),
        Interval.open(-sqrt(3), -sqrt(2)))
    assert continuous_domain(frac(x), x, S.Reals) == Complement(
        S.Reals, S.Integers)
    raises(NotImplementedError, lambda : continuous_domain(
        1/(x**2+1), x, S.Complexes))
    raises(NotImplementedError, lambda : continuous_domain(
        gamma(x), x, Interval(-5,0)))
    assert continuous_domain(x + gamma(pi), x, S.Reals) == S.Reals

