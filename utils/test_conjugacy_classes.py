
def test_conjugacy_classes():
    S = SymmetricGroup(3)
    expected = [{Permutation(size = 3)},
         {Permutation(0, 1, size = 3), Permutation(0, 2), Permutation(1, 2)},
         {Permutation(0, 1, 2), Permutation(0, 2, 1)}]
    computed = S.conjugacy_classes()

    assert len(expected) == len(computed)
    assert all(e in computed for e in expected)

