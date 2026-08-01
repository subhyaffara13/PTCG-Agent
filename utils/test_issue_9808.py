
def test_issue_9808():
    # See https://github.com/sympy/sympy/issues/16342
    assert Complement(FiniteSet(y), FiniteSet(1)) == Complement(FiniteSet(y), FiniteSet(1), evaluate=False)
    assert Complement(FiniteSet(1, 2, x), FiniteSet(x, y, 2, 3)) == \
        Complement(FiniteSet(1), FiniteSet(y), evaluate=False)

