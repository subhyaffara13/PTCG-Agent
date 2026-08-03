from typing import Union

def test_singularities():
    assert integrate(1/x**2, (x, -oo, oo)) is oo
    assert integrate(1/x**2, (x, -1, 1)) is oo
    assert integrate(1/(x - 1)**2, (x, -2, 2)) is oo

    assert integrate(1/x**2, (x, 1, -1)) is -oo
    assert integrate(1/(x - 1)**2, (x, 2, -2)) is -oo


def test_singularities():
    x = Symbol('x')
    assert singularities(x**2, x) == S.EmptySet
    assert singularities(x/(x**2 + 3*x + 2), x) == FiniteSet(-2, -1)
    assert singularities(1/(x**2 + 1), x) == FiniteSet(I, -I)
    assert singularities(x/(x**3 + 1), x) == \
        FiniteSet(-1, (1 - sqrt(3) * I) / 2, (1 + sqrt(3) * I) / 2)
    assert singularities(1/(y**2 + 2*I*y + 1), y) == \
        FiniteSet(-I + sqrt(2)*I, -I - sqrt(2)*I)
    _n = Dummy('n')
    assert singularities(sech(x), x).dummy_eq(Union(
        ImageSet(Lambda(_n, 2*_n*I*pi + I*pi/2), S.Integers),
        ImageSet(Lambda(_n, 2*_n*I*pi + 3*I*pi/2), S.Integers)))
    assert singularities(coth(x), x).dummy_eq(Union(
        ImageSet(Lambda(_n, 2*_n*I*pi + I*pi), S.Integers),
        ImageSet(Lambda(_n, 2*_n*I*pi), S.Integers)))
    assert singularities(atanh(x), x) == FiniteSet(-1, 1)
    assert singularities(acoth(x), x) == FiniteSet(-1, 1)
    assert singularities(asech(x), x) == FiniteSet(0)
    assert singularities(acsch(x), x) == FiniteSet(0)

    x = Symbol('x', real=True)
    assert singularities(1/(x**2 + 1), x) == S.EmptySet
    assert singularities(exp(1/x), x, S.Reals) == FiniteSet(0)
    assert singularities(exp(1/x), x, Interval(1, 2)) == S.EmptySet
    assert singularities(log((x - 2)**2), x, Interval(1, 3)) == FiniteSet(2)
    raises(NotImplementedError, lambda: singularities(x**-oo, x))
    assert singularities(sec(x), x, Interval(0, 3*pi)) == FiniteSet(
        pi/2, 3*pi/2, 5*pi/2)
    assert singularities(csc(x), x, Interval(0, 3*pi)) == FiniteSet(
        0, pi, 2*pi, 3*pi)

