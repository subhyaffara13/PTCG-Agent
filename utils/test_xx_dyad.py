
def test_xx_dyad():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.xx == Vector.outer(N.x, N.x)
    assert F.xx == Vector.outer(F.x, F.x)

