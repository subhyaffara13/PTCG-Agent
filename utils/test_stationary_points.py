from typing import Union

def test_stationary_points():
    assert stationary_points(sin(x), x, Interval(-pi/2, pi/2)
        ) == {-pi/2, pi/2}
    assert  stationary_points(sin(x), x, Interval.Ropen(0, pi/4)
        ) is S.EmptySet
    assert stationary_points(tan(x), x,
        ) is S.EmptySet
    assert stationary_points(sin(x)*cos(x), x, Interval(0, pi)
        ) == {pi/4, pi*Rational(3, 4)}
    assert stationary_points(sec(x), x, Interval(0, pi)
        ) == {0, pi}
    assert stationary_points((x+3)*(x-2), x
        ) == FiniteSet(Rational(-1, 2))
    assert stationary_points((x + 3)/(x - 2), x, Interval(-5, 5)
        ) is S.EmptySet
    assert stationary_points((x**2+3)/(x-2), x
        ) == {2 - sqrt(7), 2 + sqrt(7)}
    assert stationary_points((x**2+3)/(x-2), x, Interval(0, 5)
        ) == {2 + sqrt(7)}
    assert stationary_points(x**4 + x**3 - 5*x**2, x, S.Reals
        ) == FiniteSet(-2, 0, Rational(5, 4))
    assert stationary_points(exp(x), x
        ) is S.EmptySet
    assert stationary_points(log(x) - x, x, S.Reals
        ) == {1}
    assert stationary_points(cos(x), x, Union(Interval(0, 5), Interval(-6, -3))
        ) == {0, -pi, pi}
    assert stationary_points(y, x, S.Reals
        ) == S.Reals
    assert stationary_points(y, x, S.EmptySet) == S.EmptySet

