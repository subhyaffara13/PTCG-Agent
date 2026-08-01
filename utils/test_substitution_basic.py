
def test_substitution_basic():
    assert substitution([], [x, y]) == S.EmptySet
    assert substitution([], []) == S.EmptySet
    system = [2*x**2 + 3*y**2 - 30, 3*x**2 - 2*y**2 - 19]
    soln = FiniteSet((-3, -2), (-3, 2), (3, -2), (3, 2))
    assert substitution(system, [x, y]) == soln

    soln = FiniteSet((-1, 1))
    assert substitution([x + y], [x], [{y: 1}], [y], set(), [x, y]) == soln
    assert substitution(
        [x + y], [x], [{y: 1}], [y],
        {x + 1}, [y, x]) == S.EmptySet

