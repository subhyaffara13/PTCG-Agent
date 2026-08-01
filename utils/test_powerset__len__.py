
def test_powerset__len__():
    A = PowerSet(S.EmptySet, evaluate=False)
    assert len(A) == 1
    A = PowerSet(A, evaluate=False)
    assert len(A) == 2
    A = PowerSet(A, evaluate=False)
    assert len(A) == 4
    A = PowerSet(A, evaluate=False)
    assert len(A) == 16

