
def test_supplement_a_subspace_1():
    M = DM([[1, 7, 0], [2, 3, 4]], QQ).transpose()

    # First supplement over QQ:
    B = supplement_a_subspace(M)
    assert B[:, :2] == M
    assert B[:, 2] == DomainMatrix.eye(3, QQ).to_dense()[:, 0]

    # Now supplement over FF(7):
    M = M.convert_to(FF(7))
    B = supplement_a_subspace(M)
    assert B[:, :2] == M
    # When we work mod 7, first col of M goes to [1, 0, 0],
    # so the supplementary vector cannot equal this, as it did
    # when we worked over QQ. Instead, we get the second std basis vector:
    assert B[:, 2] == DomainMatrix.eye(3, FF(7)).to_dense()[:, 1]

