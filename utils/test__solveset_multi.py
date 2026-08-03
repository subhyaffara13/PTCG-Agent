from typing import Union

def test__solveset_multi():
    from sympy.solvers.solveset import _solveset_multi
    from sympy.sets import Reals

    # Basic univariate case:
    assert _solveset_multi([x**2-1], [x], [S.Reals]) == FiniteSet((1,), (-1,))

    # Linear systems of two equations
    assert _solveset_multi([x+y, x+1], [x, y], [Reals, Reals]) == FiniteSet((-1, 1))
    assert _solveset_multi([x+y, x+1], [y, x], [Reals, Reals]) == FiniteSet((1, -1))
    assert _solveset_multi([x+y, x-y-1], [x, y], [Reals, Reals]) == FiniteSet((S(1)/2, -S(1)/2))
    assert _solveset_multi([x-1, y-2], [x, y], [Reals, Reals]) == FiniteSet((1, 2))
    # assert dumeq(_solveset_multi([x+y], [x, y], [Reals, Reals]), ImageSet(Lambda(x, (x, -x)), Reals))
    assert dumeq(_solveset_multi([x+y], [x, y], [Reals, Reals]), Union(
            ImageSet(Lambda(((x,),), (x, -x)), ProductSet(Reals)),
            ImageSet(Lambda(((y,),), (-y, y)), ProductSet(Reals))))
    assert _solveset_multi([x+y, x+y+1], [x, y], [Reals, Reals]) == S.EmptySet
    assert _solveset_multi([x+y, x-y, x-1], [x, y], [Reals, Reals]) == S.EmptySet
    assert _solveset_multi([x+y, x-y, x-1], [y, x], [Reals, Reals]) == S.EmptySet

    # Systems of three equations:
    assert _solveset_multi([x+y+z-1, x+y-z-2, x-y-z-3], [x, y, z], [Reals,
        Reals, Reals]) == FiniteSet((2, -S.Half, -S.Half))

    # Nonlinear systems:
    from sympy.abc import theta
    assert _solveset_multi([x**2+y**2-2, x+y], [x, y], [Reals, Reals]) == FiniteSet((-1, 1), (1, -1))
    assert _solveset_multi([x**2-1, y], [x, y], [Reals, Reals]) == FiniteSet((1, 0), (-1, 0))
    #assert _solveset_multi([x**2-y**2], [x, y], [Reals, Reals]) == Union(
    #        ImageSet(Lambda(x, (x, -x)), Reals), ImageSet(Lambda(x, (x, x)), Reals))
    assert dumeq(_solveset_multi([x**2-y**2], [x, y], [Reals, Reals]), Union(
            ImageSet(Lambda(((x,),), (x, -Abs(x))), ProductSet(Reals)),
            ImageSet(Lambda(((x,),), (x, Abs(x))), ProductSet(Reals)),
            ImageSet(Lambda(((y,),), (-Abs(y), y)), ProductSet(Reals)),
            ImageSet(Lambda(((y,),), (Abs(y), y)), ProductSet(Reals))))
    assert _solveset_multi([r*cos(theta)-1, r*sin(theta)], [theta, r],
            [Interval(0, pi), Interval(-1, 1)]) == FiniteSet((0, 1), (pi, -1))
    assert _solveset_multi([r*cos(theta)-1, r*sin(theta)], [r, theta],
            [Interval(0, 1), Interval(0, pi)]) == FiniteSet((1, 0))
    assert _solveset_multi([r*cos(theta)-r, r*sin(theta)], [r, theta],
           [Interval(0, 1), Interval(0, pi)]) == Union(
           ImageSet(Lambda(((r,),), (r, 0)),
           ImageSet(Lambda(r, (r,)), Interval(0, 1))),
           ImageSet(Lambda(((theta,),), (0, theta)),
           ImageSet(Lambda(theta, (theta,)), Interval(0, pi))))

