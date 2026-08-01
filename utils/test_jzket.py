
def test_jzket():
    j, m = symbols('j m')
    # j not integer or half integer
    raises(ValueError, lambda: JzKet(Rational(2, 3), Rational(-1, 3)))
    raises(ValueError, lambda: JzKet(Rational(2, 3), m))
    # j < 0
    raises(ValueError, lambda: JzKet(-1, 1))
    raises(ValueError, lambda: JzKet(-1, m))
    # m not integer or half integer
    raises(ValueError, lambda: JzKet(j, Rational(-1, 3)))
    # abs(m) > j
    raises(ValueError, lambda: JzKet(1, 2))
    raises(ValueError, lambda: JzKet(1, -2))
    # j-m not integer
    raises(ValueError, lambda: JzKet(1, S.Half))

