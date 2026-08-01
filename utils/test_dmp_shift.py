
def test_dmp_shift():
    assert dmp_shift([ZZ(1), ZZ(2)], [ZZ(1)], 0, ZZ) == [ZZ(1), ZZ(3)]

    assert dmp_shift([[]], [ZZ(1), ZZ(2)], 1, ZZ) == [[]]

    xy = [[ZZ(1), ZZ(0)], []]               # x*y
    x1y2 = [[ZZ(1), ZZ(2)], [ZZ(1), ZZ(2)]] # (x+1)*(y+2)
    assert dmp_shift(xy, [ZZ(1), ZZ(2)], 1, ZZ) == x1y2

