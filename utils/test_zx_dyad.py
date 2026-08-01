
def test_zx_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.zx == Vector.outer(N.z, N.x)
    assert F.zx == Vector.outer(F.z, F.x)

