
def test_SDM_to_list():
    A = SDM({0:{1: ZZ(1)}}, (2, 2), ZZ)
    assert A.to_list() == [[ZZ(0), ZZ(1)], [ZZ(0), ZZ(0)]]

    A = SDM({}, (0, 2), ZZ)
    assert A.to_list() == []

    A = SDM({}, (2, 0), ZZ)
    assert A.to_list() == [[], []]

