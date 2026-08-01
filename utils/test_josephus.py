
def test_josephus():
    assert Permutation.josephus(4, 6, 1) == Permutation([3, 1, 0, 2, 5, 4])
    assert Permutation.josephus(1, 5, 1).is_Identity

