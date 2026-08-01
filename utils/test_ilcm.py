
def test_ilcm():
    assert ilcm(0, 0) == 0
    assert ilcm(1, 0) == 0
    assert ilcm(0, 1) == 0
    assert ilcm(1, 1) == 1
    assert ilcm(2, 1) == 2
    assert ilcm(8, 2) == 8
    assert ilcm(8, 6) == 24
    assert ilcm(8, 7) == 56
    assert ilcm(*[10, 20, 30]) == 60
    raises(ValueError, lambda: ilcm(8.1, 7))
    raises(ValueError, lambda: ilcm(8, 7.1))
    raises(TypeError, lambda: ilcm(8))

