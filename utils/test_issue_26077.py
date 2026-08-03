from typing import Union

def test_issue_26077():
    _n = Symbol('_n')
    function = x*cot(5*x)
    critical_points = stationary_points(function, x, S.Reals)
    excluded_points = Union(
        ImageSet(Lambda(_n, 2*_n*pi/5), S.Integers),
        ImageSet(Lambda(_n, 2*_n*pi/5 + pi/5), S.Integers)
    )
    solution = ConditionSet(x,
        Eq(x*(-5*cot(5*x)**2 - 5) + cot(5*x), 0),
        Complement(S.Reals, excluded_points)
    )
    assert solution.as_dummy() == critical_points.as_dummy()

