
def test_xy_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.xy == Vector.outer(N.x, N.y)
    assert F.xy == Vector.outer(F.x, F.y)

