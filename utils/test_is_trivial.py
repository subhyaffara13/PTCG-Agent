
def test_is_trivial():
    for i in range(5):
        triv = PermutationGroup([Permutation(list(range(i)))])
        assert triv.is_trivial

