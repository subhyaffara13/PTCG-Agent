
def test_ask_shuffle():
    grp = PermutationGroup(Permutation(1, 0, 2), Permutation(2, 1, 3))

    seed(123)
    first = grp.random()
    seed(123)
    simplify(I)
    second = grp.random()
    seed(123)
    simplify(-I)
    third = grp.random()

    assert first == second == third

