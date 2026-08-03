from typing import Union

def test_normalize_theta_set():
    # Interval
    assert normalize_theta_set(Interval(pi, 2*pi)) == \
        Union(FiniteSet(0), Interval.Ropen(pi, 2*pi))
    assert normalize_theta_set(Interval(pi*Rational(9, 2), 5*pi)) == Interval(pi/2, pi)
    assert normalize_theta_set(Interval(pi*Rational(-3, 2), pi/2)) == Interval.Ropen(0, 2*pi)
    assert normalize_theta_set(Interval.open(pi*Rational(-3, 2), pi/2)) == \
        Union(Interval.Ropen(0, pi/2), Interval.open(pi/2, 2*pi))
    assert normalize_theta_set(Interval.open(pi*Rational(-7, 2), pi*Rational(-3, 2))) == \
        Union(Interval.Ropen(0, pi/2), Interval.open(pi/2, 2*pi))
    assert normalize_theta_set(Interval(-pi/2, pi/2)) == \
        Union(Interval(0, pi/2), Interval.Ropen(pi*Rational(3, 2), 2*pi))
    assert normalize_theta_set(Interval.open(-pi/2, pi/2)) == \
        Union(Interval.Ropen(0, pi/2), Interval.open(pi*Rational(3, 2), 2*pi))
    assert normalize_theta_set(Interval(-4*pi, 3*pi)) == Interval.Ropen(0, 2*pi)
    assert normalize_theta_set(Interval(pi*Rational(-3, 2), -pi/2)) == Interval(pi/2, pi*Rational(3, 2))
    assert normalize_theta_set(Interval.open(0, 2*pi)) == Interval.open(0, 2*pi)
    assert normalize_theta_set(Interval.Ropen(-pi/2, pi/2)) == \
        Union(Interval.Ropen(0, pi/2), Interval.Ropen(pi*Rational(3, 2), 2*pi))
    assert normalize_theta_set(Interval.Lopen(-pi/2, pi/2)) == \
        Union(Interval(0, pi/2), Interval.open(pi*Rational(3, 2), 2*pi))
    assert normalize_theta_set(Interval(-pi/2, pi/2)) == \
        Union(Interval(0, pi/2), Interval.Ropen(pi*Rational(3, 2), 2*pi))
    assert normalize_theta_set(Interval.open(4*pi, pi*Rational(9, 2))) == Interval.open(0, pi/2)
    assert normalize_theta_set(Interval.Lopen(4*pi, pi*Rational(9, 2))) == Interval.Lopen(0, pi/2)
    assert normalize_theta_set(Interval.Ropen(4*pi, pi*Rational(9, 2))) == Interval.Ropen(0, pi/2)
    assert normalize_theta_set(Interval.open(3*pi, 5*pi)) == \
        Union(Interval.Ropen(0, pi), Interval.open(pi, 2*pi))

    # FiniteSet
    assert normalize_theta_set(FiniteSet(0, pi, 3*pi)) == FiniteSet(0, pi)
    assert normalize_theta_set(FiniteSet(0, pi/2, pi, 2*pi)) == FiniteSet(0, pi/2, pi)
    assert normalize_theta_set(FiniteSet(0, -pi/2, -pi, -2*pi)) == FiniteSet(0, pi, pi*Rational(3, 2))
    assert normalize_theta_set(FiniteSet(pi*Rational(-3, 2), pi/2)) == \
        FiniteSet(pi/2)
    assert normalize_theta_set(FiniteSet(2*pi)) == FiniteSet(0)

    # Unions
    assert normalize_theta_set(Union(Interval(0, pi/3), Interval(pi/2, pi))) == \
        Union(Interval(0, pi/3), Interval(pi/2, pi))
    assert normalize_theta_set(Union(Interval(0, pi), Interval(2*pi, pi*Rational(7, 3)))) == \
        Interval(0, pi)

    # ValueError for non-real sets
    raises(ValueError, lambda: normalize_theta_set(S.Complexes))

    # NotImplementedError for subset of reals
    raises(NotImplementedError, lambda: normalize_theta_set(Interval(0, 1)))

    # NotImplementedError without pi as coefficient
    raises(NotImplementedError, lambda: normalize_theta_set(Interval(1, 2*pi)))
    raises(NotImplementedError, lambda: normalize_theta_set(Interval(2*pi, 10)))
    raises(NotImplementedError, lambda: normalize_theta_set(FiniteSet(0, 3, 3*pi)))

