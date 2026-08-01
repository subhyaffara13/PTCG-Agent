
def test_SDM_from_list():
    A = SDM.from_list([[ZZ(0), ZZ(1)], [ZZ(1), ZZ(0)]], (2, 2), ZZ)
    assert A == SDM({0:{1:ZZ(1)}, 1:{0:ZZ(1)}}, (2, 2), ZZ)

    raises(DMBadInputError, lambda: SDM.from_list([[ZZ(0)], [ZZ(0), ZZ(1)]], (2, 2), ZZ))
    raises(DMBadInputError, lambda: SDM.from_list([[ZZ(0), ZZ(1)]], (2, 2), ZZ))

