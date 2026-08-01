
def test_deprecated_is_EmptySet():
    with warns_deprecated_sympy():
        S.EmptySet.is_EmptySet

    with warns_deprecated_sympy():
        FiniteSet(1).is_EmptySet

