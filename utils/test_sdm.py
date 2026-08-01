
def test_SDM():
    A = SDM({0:{0:ZZ(1)}}, (2, 2), ZZ)
    assert A.domain == ZZ
    assert A.shape == (2, 2)
    assert dict(A) == {0:{0:ZZ(1)}}

    raises(DMBadInputError, lambda: SDM({5:{1:ZZ(0)}}, (2, 2), ZZ))
    raises(DMBadInputError, lambda: SDM({0:{5:ZZ(0)}}, (2, 2), ZZ))

