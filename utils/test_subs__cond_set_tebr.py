
def test_subs_CondSet_tebr():
    with warns_deprecated_sympy():
        assert ConditionSet((x, y), {x + 1, x + y}, S.Reals**2) == \
            ConditionSet((x, y), Eq(x + 1, 0) & Eq(x + y, 0), S.Reals**2)

