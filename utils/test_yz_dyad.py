
def test_yz_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.yz == Vector.outer(N.y, N.z)
    assert F.yz == Vector.outer(F.y, F.z)

