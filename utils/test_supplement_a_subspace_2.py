
def test_supplement_a_subspace_2():
    M = DM([[1, 0, 0], [2, 0, 0]], QQ).transpose()
    with raises(DMRankError):
        supplement_a_subspace(M)

