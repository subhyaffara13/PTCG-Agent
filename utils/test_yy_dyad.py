
def test_yy_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.yy == Vector.outer(N.y, N.y)
    assert F.yy == Vector.outer(F.y, F.y)

