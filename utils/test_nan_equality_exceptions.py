
def test_nan_equality_exceptions():
    # See issue #7774
    import random
    assert Equality(nan, nan) is S.false
    assert Unequality(nan, nan) is S.true

    # See issue #7773
    A = (x, S.Zero, S.One/3, pi, oo, -oo)
    assert Equality(nan, random.choice(A)) is S.false
    assert Equality(random.choice(A), nan) is S.false
    assert Unequality(nan, random.choice(A)) is S.true
    assert Unequality(random.choice(A), nan) is S.true

