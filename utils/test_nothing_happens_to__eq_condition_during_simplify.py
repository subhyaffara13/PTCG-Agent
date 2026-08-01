
def test_nothing_happens_to_Eq_condition_during_simplify():
    # issue 25701
    r = symbols('r', real=True)
    assert Eq(2*sign(r + 3)/(5*Abs(r + 3)**Rational(3, 5)), 0
        ).simplify() == Eq(Piecewise(
        (0, Eq(r, -3)), ((r + 3)/(5*Abs((r + 3)**Rational(8, 5)))*2, True)), 0)

