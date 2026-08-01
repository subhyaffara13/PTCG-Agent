
def test_zy_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.zy == Vector.outer(N.z, N.y)
    assert F.zy == Vector.outer(F.z, F.y)

