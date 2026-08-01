
def test_permutation_equality():
    a = Permutation(0, 1, 2)
    b = Permutation(0, 1, 2)
    assert Eq(a, b) is S.true
    c = Permutation(0, 2, 1)
    assert Eq(a, c) is S.false

    d = Permutation(0, 1, 2, size=4)
    assert unchanged(Eq, a, d)
    e = Permutation(0, 2, 1, size=4)
    assert unchanged(Eq, a, e)

    i = Permutation()
    assert unchanged(Eq, i, 0)
    assert unchanged(Eq, 0, i)

