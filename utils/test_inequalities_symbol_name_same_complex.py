
def test_inequalities_symbol_name_same_complex():
    """Using the operator and functional forms should give same results.
    With complex non-real numbers, both should raise errors.
    """
    # FIXME: could replace with random selection after test passes
    for a in (x, S.Zero, S.One/3, pi, oo, Rational(1, 3)):
        raises(TypeError, lambda: Gt(a, I))
        raises(TypeError, lambda: a > I)
        raises(TypeError, lambda: Lt(a, I))
        raises(TypeError, lambda: a < I)
        raises(TypeError, lambda: Ge(a, I))
        raises(TypeError, lambda: a >= I)
        raises(TypeError, lambda: Le(a, I))
        raises(TypeError, lambda: a <= I)

