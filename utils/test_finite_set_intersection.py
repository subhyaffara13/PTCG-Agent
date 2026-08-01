
def test_finite_set_intersection():
    # The following should not produce recursion errors
    # Note: some of these are not completely correct. See
    # https://github.com/sympy/sympy/issues/16342.
    assert Intersection(FiniteSet(-oo, x), FiniteSet(x)) == FiniteSet(x)
    assert Intersection._handle_finite_sets([FiniteSet(-oo, x), FiniteSet(0, x)]) == FiniteSet(x)

    assert Intersection._handle_finite_sets([FiniteSet(-oo, x), FiniteSet(x)]) == FiniteSet(x)
    assert Intersection._handle_finite_sets([FiniteSet(2, 3, x, y), FiniteSet(1, 2, x)]) == \
        Intersection._handle_finite_sets([FiniteSet(1, 2, x), FiniteSet(2, 3, x, y)]) == \
        Intersection(FiniteSet(1, 2, x), FiniteSet(2, 3, x, y)) == \
        Intersection(FiniteSet(1, 2, x), FiniteSet(2, x, y))

    assert FiniteSet(1+x-y) & FiniteSet(1) == \
        FiniteSet(1) & FiniteSet(1+x-y) == \
        Intersection(FiniteSet(1+x-y), FiniteSet(1), evaluate=False)

    assert FiniteSet(1) & FiniteSet(x) == FiniteSet(x) & FiniteSet(1) == \
        Intersection(FiniteSet(1), FiniteSet(x), evaluate=False)

    assert FiniteSet({x}) & FiniteSet({x, y}) == \
        Intersection(FiniteSet({x}), FiniteSet({x, y}), evaluate=False)

