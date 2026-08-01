
def test_powerset_contains():
    A = PowerSet(FiniteSet(1), evaluate=False)
    assert A.contains(2) == Contains(2, A)

    x = Symbol('x')

    A = PowerSet(FiniteSet(x), evaluate=False)
    assert A.contains(FiniteSet(1)) == Contains(FiniteSet(1), A)

