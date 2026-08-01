
def test_zz_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.zz == Vector.outer(N.z, N.z)
    assert F.zz == Vector.outer(F.z, F.z)

