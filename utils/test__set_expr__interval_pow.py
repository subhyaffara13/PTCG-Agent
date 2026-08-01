
def test_SetExpr_Interval_pow():
    assert SetExpr(Interval(0, 2))**2 == SetExpr(Interval(0, 4))
    assert SetExpr(Interval(-1, 1))**2 == SetExpr(Interval(0, 1))
    assert SetExpr(Interval(1, 2))**2 == SetExpr(Interval(1, 4))
    assert SetExpr(Interval(-1, 2))**3 == SetExpr(Interval(-1, 8))
    assert SetExpr(Interval(-1, 1))**0 == SetExpr(FiniteSet(1))


    assert SetExpr(Interval(1, 2))**Rational(5, 2) == SetExpr(Interval(1, 4*sqrt(2)))
    #assert SetExpr(Interval(-1, 2))**Rational(1, 3) == SetExpr(Interval(-1, 2**Rational(1, 3)))
    #assert SetExpr(Interval(0, 2))**S.Half == SetExpr(Interval(0, sqrt(2)))

    #assert SetExpr(Interval(-4, 2))**Rational(2, 3) == SetExpr(Interval(0, 2*2**Rational(1, 3)))

    #assert SetExpr(Interval(-1, 5))**S.Half == SetExpr(Interval(0, sqrt(5)))
    #assert SetExpr(Interval(-oo, 2))**S.Half == SetExpr(Interval(0, sqrt(2)))
    #assert SetExpr(Interval(-2, 3))**(Rational(-1, 4)) == SetExpr(Interval(0, oo))

    assert SetExpr(Interval(1, 5))**(-2) == SetExpr(Interval(Rational(1, 25), 1))
    assert SetExpr(Interval(-1, 3))**(-2) == SetExpr(Interval(0, oo))

    assert SetExpr(Interval(0, 2))**(-2) == SetExpr(Interval(Rational(1, 4), oo))
    assert SetExpr(Interval(-1, 2))**(-3) == SetExpr(Union(Interval(-oo, -1), Interval(Rational(1, 8), oo)))
    assert SetExpr(Interval(-3, -2))**(-3) == SetExpr(Interval(Rational(-1, 8), Rational(-1, 27)))
    assert SetExpr(Interval(-3, -2))**(-2) == SetExpr(Interval(Rational(1, 9), Rational(1, 4)))
    #assert SetExpr(Interval(0, oo))**S.Half == SetExpr(Interval(0, oo))
    #assert SetExpr(Interval(-oo, -1))**Rational(1, 3) == SetExpr(Interval(-oo, -1))
    #assert SetExpr(Interval(-2, 3))**(Rational(-1, 3)) == SetExpr(Interval(-oo, oo))

    assert SetExpr(Interval(-oo, 0))**(-2) == SetExpr(Interval.open(0, oo))
    assert SetExpr(Interval(-2, 0))**(-2) == SetExpr(Interval(Rational(1, 4), oo))

    assert SetExpr(Interval(Rational(1, 3), S.Half))**oo == SetExpr(FiniteSet(0))
    assert SetExpr(Interval(0, S.Half))**oo == SetExpr(FiniteSet(0))
    assert SetExpr(Interval(S.Half, 1))**oo == SetExpr(Interval(0, oo))
    assert SetExpr(Interval(0, 1))**oo == SetExpr(Interval(0, oo))
    assert SetExpr(Interval(2, 3))**oo == SetExpr(FiniteSet(oo))
    assert SetExpr(Interval(1, 2))**oo == SetExpr(Interval(0, oo))
    assert SetExpr(Interval(S.Half, 3))**oo == SetExpr(Interval(0, oo))
    assert SetExpr(Interval(Rational(-1, 3), Rational(-1, 4)))**oo == SetExpr(FiniteSet(0))
    assert SetExpr(Interval(-1, Rational(-1, 2)))**oo == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(-3, -2))**oo == SetExpr(FiniteSet(-oo, oo))
    assert SetExpr(Interval(-2, -1))**oo == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(-2, Rational(-1, 2)))**oo == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(Rational(-1, 2), S.Half))**oo == SetExpr(FiniteSet(0))
    assert SetExpr(Interval(Rational(-1, 2), 1))**oo == SetExpr(Interval(0, oo))
    assert SetExpr(Interval(Rational(-2, 3), 2))**oo == SetExpr(Interval(0, oo))
    assert SetExpr(Interval(-1, 1))**oo == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(-1, S.Half))**oo == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(-1, 2))**oo == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(-2, S.Half))**oo == SetExpr(Interval(-oo, oo))

    assert (SetExpr(Interval(1, 2))**x).dummy_eq(SetExpr(ImageSet(Lambda(_d, _d**x), Interval(1, 2))))

    assert SetExpr(Interval(2, 3))**(-oo) == SetExpr(FiniteSet(0))
    assert SetExpr(Interval(0, 2))**(-oo) == SetExpr(Interval(0, oo))
    assert (SetExpr(Interval(-1, 2))**(-oo)).dummy_eq(SetExpr(ImageSet(Lambda(_d, _d**(-oo)), Interval(-1, 2))))

