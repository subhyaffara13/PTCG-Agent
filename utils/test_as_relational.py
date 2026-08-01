
def test_as_relational():
    assert ConditionSet((x, y), x > 1, S.Integers**2).as_relational((x, y)
        ) == (x > 1) & Contains(x, S.Integers) & Contains(y, S.Integers)
    assert ConditionSet(x, x > 1, S.Integers).as_relational(x
        ) == Contains(x, S.Integers) & (x > 1)

