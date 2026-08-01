
def test_DomainMatrix_clear_denoms():
    A = DM([[(1,2),(1,3)],[(1,4),(1,5)]], QQ)

    den_Z = DomainScalar(ZZ(60), ZZ)
    Anum_Z = DM([[30, 20], [15, 12]], ZZ)
    Anum_Q = Anum_Z.convert_to(QQ)

    assert A.clear_denoms() == (den_Z, Anum_Q)
    assert A.clear_denoms(convert=True) == (den_Z, Anum_Z)
    assert A * den_Z == Anum_Q
    assert A == Anum_Q / den_Z

