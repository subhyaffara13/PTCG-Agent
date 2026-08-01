
def test_bound_symbols():
    assert ConditionSet(x, Eq(y, 0), FiniteSet(z)
        ).bound_symbols == [x]
    assert ConditionSet(x, Eq(x, 0), FiniteSet(x, y)
        ).bound_symbols == [x]
    assert ConditionSet(x, x < 10, ImageSet(Lambda(y, y**2), S.Integers)
        ).bound_symbols == [x]
    assert ConditionSet(x, x < 10, ConditionSet(y, y > 1, S.Integers)
        ).bound_symbols == [x]

