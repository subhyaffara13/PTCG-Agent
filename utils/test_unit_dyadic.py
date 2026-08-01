
def test_unit_dyadic():
    N = ReferenceFrame('N')
    F = ReferenceFrame('F', indices=['1', '2', '3'])
    assert N.u == N.xx + N.yy + N.zz
    assert F.u == F.xx + F.yy + F.zz

