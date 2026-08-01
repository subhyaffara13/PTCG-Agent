
def test_as_explicit_matrix():
    A = ImmutableMatrix([[1, 2], [3, 4]])
    assert MatPow(A, 0).as_explicit() == ImmutableMatrix(Identity(2))
    assert MatPow(A, 1).as_explicit() == A
    assert MatPow(A, 2).as_explicit() == A**2
    assert MatPow(A, -1).as_explicit() == A.inv()
    assert MatPow(A, -2).as_explicit() == (A.inv())**2
    # less expensive than testing on a 2x2
    A = ImmutableMatrix([4])
    assert MatPow(A, S.Half).as_explicit() == A**S.Half

