
def test_CondSet():
    sin_sols_principal = ConditionSet(x, Eq(sin(x), 0),
                                      Interval(0, 2*pi, False, True))
    assert pi in sin_sols_principal
    assert pi/2 not in sin_sols_principal
    assert 3*pi not in sin_sols_principal
    assert oo not in sin_sols_principal
    assert 5 in ConditionSet(x, x**2 > 4, S.Reals)
    assert 1 not in ConditionSet(x, x**2 > 4, S.Reals)
    # in this case, 0 is not part of the base set so
    # it can't be in any subset selected by the condition
    assert 0 not in ConditionSet(x, y > 5, Interval(1, 7))
    # since 'in' requires a true/false, the following raises
    # an error because the given value provides no information
    # for the condition to evaluate (since the condition does
    # not depend on the dummy symbol): the result is `y > 5`.
    # In this case, ConditionSet is just acting like
    # Piecewise((Interval(1, 7), y > 5), (S.EmptySet, True)).
    raises(TypeError, lambda: 6 in ConditionSet(x, y > 5,
        Interval(1, 7)))

    X = MatrixSymbol('X', 2, 2)
    matrix_set = ConditionSet(X, Eq(X*Matrix([[1, 1], [1, 1]]), X))
    Y = Matrix([[0, 0], [0, 0]])
    assert matrix_set.contains(Y).doit() is S.true
    Z = Matrix([[1, 2], [3, 4]])
    assert matrix_set.contains(Z).doit() is S.false

    assert isinstance(ConditionSet(x, x < 1, {x, y}).base_set,
        FiniteSet)
    raises(TypeError, lambda: ConditionSet(x, x + 1, {x, y}))
    raises(TypeError, lambda: ConditionSet(x, x, 1))

    I = S.Integers
    U = S.UniversalSet
    C = ConditionSet
    assert C(x, False, I) is S.EmptySet
    assert C(x, True, I) is I
    assert C(x, x < 1, C(x, x < 2, I)
        ) == C(x, (x < 1) & (x < 2), I)
    assert C(y, y < 1, C(x, y < 2, I)
        ) == C(x, (x < 1) & (y < 2), I), C(y, y < 1, C(x, y < 2, I))
    assert C(y, y < 1, C(x, x < 2, I)
        ) == C(y, (y < 1) & (y < 2), I)
    assert C(y, y < 1, C(x, y < x, I)
        ) == C(x, (x < 1) & (y < x), I)
    assert unchanged(C, y, x < 1, C(x, y < x, I))
    assert ConditionSet(x, x < 1).base_set is U
    # arg checking is not done at instantiation but this
    # will raise an error when containment is tested
    assert ConditionSet((x,), x < 1).base_set is U

    c = ConditionSet((x, y), x < y, I**2)
    assert (1, 2) in c
    assert (1, pi) not in c

    raises(TypeError, lambda: C(x, x > 1, C((x, y), x > 1, I**2)))
    # signature mismatch since only 3 args are accepted
    raises(TypeError, lambda: C((x, y), x + y < 2, U, U))

