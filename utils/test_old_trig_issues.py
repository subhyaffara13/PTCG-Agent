from typing import Union

def test_old_trig_issues():
    # issues #9606 / #9531:
    assert solveset(sinh(x), x, S.Reals) == FiniteSet(0)
    assert solveset(sinh(x), x, S.Complexes).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*I*pi), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi + I*pi), S.Integers)))

    # issues #11218 / #18427
    assert solveset(sin(pi*x), x, S.Reals).dummy_eq(Union(
        ImageSet(Lambda(n, (2*n*pi + pi)/pi), S.Integers),
        ImageSet(Lambda(n, 2*n), S.Integers)))
    assert solveset(sin(pi*x), x).dummy_eq(Union(
        ImageSet(Lambda(n, (2*n*pi + pi)/pi), S.Integers),
        ImageSet(Lambda(n, 2*n), S.Integers)))

    # issue #17543
    assert solveset(I*cot(8*x - 8*E), x).dummy_eq(
        ImageSet(Lambda(n, pi*n/8 - 13*pi/16 + E), S.Integers))

    # issue #20798
    assert all_close(solveset(cos(2*x) - 0.5, x, Interval(0, 2*pi)), FiniteSet(
        0.523598775598299, -0.523598775598299 + pi,
        -0.523598775598299 + 2*pi, 0.523598775598299 + pi))
    sol = Union(ImageSet(Lambda(n, n*pi - 0.523598775598299), S.Integers),
                ImageSet(Lambda(n, n*pi + 0.523598775598299), S.Integers))
    ret = solveset(cos(2*x) - 0.5, x, S.Reals)
    # replace Dummy n by the regular Symbol n to allow all_close comparison.
    ret = ret.subs(ret.atoms(Dummy).pop(), n)
    assert all_close(ret, sol)
    ret = solveset(cos(2*x) - 0.5, x, S.Complexes)
    ret = ret.subs(ret.atoms(Dummy).pop(), n)
    assert all_close(ret, sol)

    # issue #21296 / #17667
    assert solveset(tan(x)-sqrt(2), x, Interval(0, pi/2)) == FiniteSet(atan(sqrt(2)))
    assert solveset(tan(x)-pi, x, Interval(0, pi/2)) == FiniteSet(atan(pi))

    # issue #17667
    # not yet working properly:
    # solveset(cos(x)-y, x, Interval(0, pi))
    assert solveset(cos(x)-y, x, S.Reals).dummy_eq(
        ConditionSet(x,(S(-1) <= y) & (y <= S(1)), Union(
            ImageSet(Lambda(n, 2*n*pi - acos(y)), S.Integers),
            ImageSet(Lambda(n, 2*n*pi + acos(y)), S.Integers))))

    # issue #17579
    # Valid result, but the intersection could potentially be simplified.
    assert solveset(sin(log(x)), x, Interval(0,1, True, False)).dummy_eq(
        Union(Intersection(ImageSet(Lambda(n, exp(2*n*pi)), S.Integers), Interval.Lopen(0, 1)),
              Intersection(ImageSet(Lambda(n, exp(2*n*pi + pi)), S.Integers), Interval.Lopen(0, 1))))

    # issue #17334
    assert solveset(sin(x) - sin(1), x, S.Reals).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*pi + 1), S.Integers),
        ImageSet(Lambda(n, 2*n*pi - 1 + pi), S.Integers)))
    assert solveset(sin(x) - sqrt(5)/3, x, S.Reals).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*pi + asin(sqrt(5)/3)), S.Integers),
        ImageSet(Lambda(n, 2*n*pi - asin(sqrt(5)/3) + pi), S.Integers)))
    assert solveset(sinh(x)-cosh(2), x, S.Reals) == FiniteSet(asinh(cosh(2)))

    # issue 9825
    assert solveset(Eq(tan(x), y), x, domain=S.Reals).dummy_eq(
        ConditionSet(x, (-oo < y) & (y < oo),
                     ImageSet(Lambda(n, n*pi + atan(y)), S.Integers)))
    r = Symbol('r', real=True)
    assert solveset(Eq(tan(x), r), x, domain=S.Reals).dummy_eq(
        ImageSet(Lambda(n, n*pi + atan(r)), S.Integers))

