
def test_make_perm():
    assert cube.pgroup.make_perm(5, seed=list(range(5))) == \
        Permutation([4, 7, 6, 5, 0, 3, 2, 1])
    assert cube.pgroup.make_perm(7, seed=list(range(7))) == \
        Permutation([6, 7, 3, 2, 5, 4, 0, 1])

