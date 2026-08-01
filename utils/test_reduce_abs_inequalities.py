
def test_reduce_abs_inequalities():
    e = abs(x - 5) < 3
    ans = And(Lt(2, x), Lt(x, 8))
    assert reduce_inequalities(e) == ans
    assert reduce_inequalities(e, x) == ans
    assert reduce_inequalities(abs(x - 5)) == Eq(x, 5)
    assert reduce_inequalities(
        abs(2*x + 3) >= 8) == Or(And(Le(Rational(5, 2), x), Lt(x, oo)),
        And(Le(x, Rational(-11, 2)), Lt(-oo, x)))
    assert reduce_inequalities(abs(x - 4) + abs(
        3*x - 5) < 7) == And(Lt(S.Half, x), Lt(x, 4))
    assert reduce_inequalities(abs(x - 4) + abs(3*abs(x) - 5) < 7) == \
        Or(And(S(-2) < x, x < -1), And(S.Half < x, x < 4))

    nr = Symbol('nr', extended_real=False)
    raises(TypeError, lambda: reduce_inequalities(abs(nr - 5) < 3))
    assert reduce_inequalities(x < 3, symbols=[x, nr]) == And(-oo < x, x < 3)

