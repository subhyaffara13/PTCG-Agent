
def test_DomainMatrix_clear_denoms_rowwise():
    A = DM([[(1,2),(1,3)],[(1,4),(1,5)]], QQ)

    den_Z = DM([[6, 0], [0, 20]], ZZ).to_sparse()
    Anum_Z = DM([[3, 2], [5, 4]], ZZ)
    Anum_Q = DM([[3, 2], [5, 4]], QQ)

    assert A.clear_denoms_rowwise() == (den_Z, Anum_Q)
    assert A.clear_denoms_rowwise(convert=True) == (den_Z, Anum_Z)
    assert den_Z * A == Anum_Q
    assert A == den_Z.to_field().inv() * Anum_Q

    A = DM([[(1,2),(1,3),0,0],[0,0,0,0], [(1,4),(1,5),(1,6),(1,7)]], QQ)
    den_Z = DM([[6, 0, 0], [0, 1, 0], [0, 0, 420]], ZZ).to_sparse()
    Anum_Z = DM([[3, 2, 0, 0], [0, 0, 0, 0], [105, 84, 70, 60]], ZZ)
    Anum_Q = Anum_Z.convert_to(QQ)

    assert A.clear_denoms_rowwise() == (den_Z, Anum_Q)
    assert A.clear_denoms_rowwise(convert=True) == (den_Z, Anum_Z)
    assert den_Z * A == Anum_Q
    assert A == den_Z.to_field().inv() * Anum_Q

