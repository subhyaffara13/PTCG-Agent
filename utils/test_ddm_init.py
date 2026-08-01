
def test_DDM_init():
    items = [[ZZ(0), ZZ(1), ZZ(2)], [ZZ(3), ZZ(4), ZZ(5)]]
    shape = (2, 3)
    ddm = DDM(items, shape, ZZ)
    assert ddm.shape == shape
    assert ddm.rows == 2
    assert ddm.cols == 3
    assert ddm.domain == ZZ

    raises(DMBadInputError, lambda: DDM([[ZZ(2), ZZ(3)]], (2, 2), ZZ))
    raises(DMBadInputError, lambda: DDM([[ZZ(1)], [ZZ(2), ZZ(3)]], (2, 2), ZZ))

