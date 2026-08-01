
def test_O10():
    L = [Matrix([2, 3, 5]), Matrix([3, 6, 2]), Matrix([8, 3, 6])]
    assert GramSchmidt(L) == [Matrix([
                              [2],
                              [3],
                              [5]]),
                              Matrix([
                              [R(23, 19)],
                              [R(63, 19)],
                              [R(-47, 19)]]),
                              Matrix([
                              [R(1692, 353)],
                              [R(-1551, 706)],
                              [R(-423, 706)]])]

