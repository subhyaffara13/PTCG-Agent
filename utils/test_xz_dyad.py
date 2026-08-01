
def test_xz_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.xz == Vector.outer(N.x, N.z)
    assert F.xz == Vector.outer(F.x, F.z)

