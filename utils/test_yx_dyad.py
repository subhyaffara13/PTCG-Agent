
def test_yx_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.yx == Vector.outer(N.y, N.x)
    assert F.yx == Vector.outer(F.y, F.x)

