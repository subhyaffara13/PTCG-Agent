
def test_garbage_input():
    raises(ValueError, lambda: solveset_real([y], y))
    x = Symbol('x', real=True)
    assert solveset_real(x, 1) == S.EmptySet
    assert solveset_real(x - 1, 1) == FiniteSet(x)
    assert solveset_real(x, pi) == S.EmptySet
    assert solveset_real(x, x**2) == S.EmptySet

    raises(ValueError, lambda: solveset_complex([x], x))
    assert solveset_complex(x, pi) == S.EmptySet

    raises(ValueError, lambda: solveset((x, y), x))
    raises(ValueError, lambda: solveset(x + 1, S.Reals))
    raises(ValueError, lambda: solveset(x + 1, x, 2))

