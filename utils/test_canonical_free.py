
def test_canonical_free():
    # t = A^{d0 a1}*A_d0^a0
    # ord = [a0,a1,d0,-d0];  g = [2,1,3,0,4,5]; dummies = [[2,3]]
    # t_c = A_d0^a0*A^{d0 a1}
    # can = [3,0, 2,1, 4,5]
    g = Permutation([2,1,3,0,4,5])
    dummies = [[2,3]]
    can = canonicalize(g, dummies, [None], ([], [Permutation(3)], 2, 0))
    assert can == [3,0, 2,1, 4,5]

