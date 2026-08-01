
def test_finite_basic():
    x = Symbol('x')
    A = FiniteSet(1, 2, 3)
    B = FiniteSet(3, 4, 5)
    AorB = Union(A, B)
    AandB = A.intersect(B)
    assert A.is_subset(AorB) and B.is_subset(AorB)
    assert AandB.is_subset(A)
    assert AandB == FiniteSet(3)

    assert A.inf == 1 and A.sup == 3
    assert AorB.inf == 1 and AorB.sup == 5
    assert FiniteSet(x, 1, 5).sup == Max(x, 5)
    assert FiniteSet(x, 1, 5).inf == Min(x, 1)

    # issue 7335
    assert FiniteSet(S.EmptySet) != S.EmptySet
    assert FiniteSet(FiniteSet(1, 2, 3)) != FiniteSet(1, 2, 3)
    assert FiniteSet((1, 2, 3)) != FiniteSet(1, 2, 3)

    # Ensure a variety of types can exist in a FiniteSet
    assert FiniteSet((1, 2), A, -5, x, 'eggs', x**2)

    assert (A > B) is False
    assert (A >= B) is False
    assert (A < B) is False
    assert (A <= B) is False
    assert AorB > A and AorB > B
    assert AorB >= A and AorB >= B
    assert A >= A and A <= A
    assert A >= AandB and B >= AandB
    assert A > AandB and B > AandB

