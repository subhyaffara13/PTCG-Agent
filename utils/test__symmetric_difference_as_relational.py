
def test_SymmetricDifference_as_relational():
    x = Symbol('x')
    expr = SymmetricDifference(Interval(0, 1), FiniteSet(2), evaluate=False)
    assert expr.as_relational(x) == Xor(Eq(x, 2), Le(0, x) & Le(x, 1))

